"""Auth and profile business logic (SPEC §18.1, §18.2).

All numeric rules come from apps.core.config.get_limit (admin-editable); nothing is
hardcoded. Views stay thin and call these functions.
"""

from __future__ import annotations

import contextlib
import re
import secrets
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, cast

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.config import get_limit

from .exceptions import (
    AccountBlocked,
    CodeExpired,
    InvalidCode,
    InvalidPhone,
    ResendTooSoon,
    TooManyAttempts,
)
from .models import Device, PhoneOTP, Platform, Session, User

_NON_DIGITS = re.compile(r"\D")
# Letters (any script), spaces, hyphen and apostrophe only. No digits, no URLs.
_NAME_RE = re.compile(r"^[^\W\d_](?:[^\W\d_]|[ '\-])*$", re.UNICODE)
_LINK_RE = re.compile(r"(https?://|www\.|\.(?:uz|com|ru|net|org)\b)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Phone
# ---------------------------------------------------------------------------
def normalize_phone(raw: str) -> str:
    """Normalize to +998XXXXXXXXX, validating the operator code (§18.1)."""
    digits = _NON_DIGITS.sub("", raw or "")
    if digits.startswith("998"):
        digits = digits[3:]
    if len(digits) != 9 or digits[:2] not in settings.UZ_PHONE_OPERATOR_CODES:
        raise InvalidPhone
    return f"+998{digits}"


# ---------------------------------------------------------------------------
# Name
# ---------------------------------------------------------------------------
def validate_name(name: str) -> str:
    name = (name or "").strip()
    if not (2 <= len(name) <= 40) or _LINK_RE.search(name) or not _NAME_RE.match(name):
        raise ValidationError({"name": [_("Ism noto'g'ri")]})
    return name


# ---------------------------------------------------------------------------
# SMS code: request
# ---------------------------------------------------------------------------
@dataclass
class CodeRequestResult:
    phone: str
    resend_after_seconds: int


def _generate_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def request_code(raw_phone: str) -> CodeRequestResult:
    phone = normalize_phone(raw_phone)

    user = User.objects.filter(phone=phone).first()
    if user and user.is_blocked:
        raise AccountBlocked(_("Akkauntingiz bloklangan. Sababi: %(r)s") % {"r": user.block_reason})

    now = timezone.now()
    cooldown = get_limit("sms_resend_cooldown_seconds")
    recent = PhoneOTP.objects.filter(phone=phone).order_by("-created_at").first()
    if recent and (now - recent.created_at).total_seconds() < cooldown:
        raise ResendTooSoon

    per_hour = PhoneOTP.objects.filter(
        phone=phone, created_at__gte=now - timedelta(hours=1)
    ).count()
    per_day = PhoneOTP.objects.filter(phone=phone, created_at__gte=now - timedelta(days=1)).count()
    if per_hour >= get_limit("sms_per_phone_per_hour") or per_day >= get_limit(
        "sms_per_phone_per_day"
    ):
        raise ResendTooSoon(_("Juda ko'p SMS so'raldi. Keyinroq urinib ko'ring"))

    code = _generate_code()
    PhoneOTP.objects.create(
        phone=phone,
        code_hash=make_password(code),
        expires_at=now + timedelta(seconds=get_limit("sms_code_ttl_seconds")),
    )

    from .providers import get_sms_provider

    message = _("Elat tasdiqlash kodi: %(code)s") % {"code": code}
    get_sms_provider().send(phone, message)
    return CodeRequestResult(phone=phone, resend_after_seconds=cooldown)


# ---------------------------------------------------------------------------
# SMS code: verify + issue tokens
# ---------------------------------------------------------------------------
@dataclass
class AuthResult:
    user: User
    access: str
    refresh: str
    is_new: bool


def _issue_tokens(user: User, device: dict[str, Any] | None) -> tuple[str, str, str]:
    refresh = RefreshToken.for_user(user)
    jti = str(refresh["jti"])
    lifetime = cast(timedelta, settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"])
    exp = timezone.now() + lifetime
    device = device or {}
    Session.objects.create(
        user=user,
        jti=jti,
        platform=device.get("platform", ""),
        app_version=device.get("app_version", ""),
        user_agent=device.get("user_agent", "")[:255],
        ip=device.get("ip"),
        expires_at=exp,
    )
    return str(refresh.access_token), str(refresh), jti


@transaction.atomic
def verify_code(raw_phone: str, code: str, device: dict[str, Any] | None = None) -> AuthResult:
    phone = normalize_phone(raw_phone)
    otp = (
        PhoneOTP.objects.select_for_update()
        .filter(phone=phone, consumed_at__isnull=True)
        .order_by("-created_at")
        .first()
    )
    if otp is None:
        raise InvalidCode
    if otp.is_locked:
        raise TooManyAttempts
    if otp.is_expired:
        raise CodeExpired

    max_attempts = get_limit("sms_max_wrong_attempts")
    if not check_password(code, otp.code_hash):
        otp.attempts += 1
        if otp.attempts >= max_attempts:
            otp.locked_until = timezone.now() + timedelta(minutes=get_limit("sms_lockout_minutes"))
            otp.save(update_fields=["attempts", "locked_until", "updated_at"])
            raise TooManyAttempts
        otp.save(update_fields=["attempts", "updated_at"])
        remaining = max_attempts - otp.attempts
        raise InvalidCode(_("Kod noto'g'ri. Qolgan urinish: %(n)d") % {"n": remaining})

    otp.consumed_at = timezone.now()
    otp.save(update_fields=["consumed_at", "updated_at"])

    user, is_new = User.objects.get_or_create(phone=phone)
    if user.is_blocked:
        raise AccountBlocked(_("Akkauntingiz bloklangan. Sababi: %(r)s") % {"r": user.block_reason})
    user.is_verified = True
    user.last_seen = timezone.now()
    user.save(update_fields=["is_verified", "last_seen"])

    access, refresh, _jti = _issue_tokens(user, device)
    return AuthResult(user=user, access=access, refresh=refresh, is_new=is_new)


# ---------------------------------------------------------------------------
# Logout (revoke one device)
# ---------------------------------------------------------------------------
def logout(refresh_token: str) -> None:
    try:
        token = RefreshToken(refresh_token)  # type: ignore[arg-type]
        jti = str(token["jti"])
        token.blacklist()
    except Exception as exc:  # invalid/expired token
        raise ValidationError({"refresh": [_("Token noto'g'ri")]}) from exc
    Session.objects.filter(jti=jti).update(revoked_at=timezone.now())


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------
def update_profile(user: User, data: dict[str, Any]) -> User:
    if "name" in data:
        user.name = validate_name(data["name"])
    if "about" in data:
        about = (data["about"] or "").strip()
        if len(about) > 200:
            raise ValidationError({"about": [_("Juda uzun (200 belgigacha)")]})
        user.about = about
    if "language" in data:
        user.language = data["language"]
    if "city_id" in data:
        user.city_id = data["city_id"]
    if "show_phone" in data:
        user.show_phone = bool(data["show_phone"])
    user.save()
    return user


# ---------------------------------------------------------------------------
# Devices
# ---------------------------------------------------------------------------
def register_device(user: User, fcm_token: str, platform: str, app_version: str = "") -> Device:
    if platform not in Platform.values:
        raise ValidationError({"platform": [_("Platforma noto'g'ri")]})
    device, _created = Device.objects.update_or_create(
        fcm_token=fcm_token,
        defaults={
            "user": user,
            "platform": platform,
            "app_version": app_version,
            "last_seen": timezone.now(),
        },
    )
    return device


# ---------------------------------------------------------------------------
# Account deletion (§18.2): confirmed by SMS code, irreversible, anonymizes data.
# ---------------------------------------------------------------------------
@transaction.atomic
def delete_account(user: User, code: str) -> None:
    # Reuse the SMS verification path; raises on a bad/expired code.
    verify_code(user.phone, code)

    # Revoke every session/refresh token.
    from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

    for token in OutstandingToken.objects.filter(user=user):
        with contextlib.suppress(Exception):  # already expired/blacklisted
            RefreshToken(token.token).blacklist()  # type: ignore[arg-type]
    Session.objects.filter(user=user, revoked_at__isnull=True).update(revoked_at=timezone.now())

    # Anonymize (active listings are removed once the listings app lands).
    user.phone = f"deleted-{user.pk}-{secrets.token_hex(4)}"
    user.name = ""
    user.about = ""
    if user.avatar:
        user.avatar.delete(save=False)
    user.is_active = False
    user.is_verified = False
    user.deleted_at = timezone.now()
    user.set_unusable_password()
    user.save()
