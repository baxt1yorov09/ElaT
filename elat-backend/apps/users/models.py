"""Users: phone-based account, SMS one-time codes, devices and sessions.

AUTH_USER_MODEL is set to users.User before the first migration (Django pitfall).
Normal users have no password (SMS login); staff/superusers keep passwords for admin.
Numeric rules (code TTL, attempts, lockout) live in SPEC §18.1 and apps.core.config,
never hardcoded here.
"""

from __future__ import annotations

from typing import ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Role(models.TextChoices):
    GUEST = "guest", _("Guest")
    USER = "user", _("User")
    BUSINESS = "business", _("Business profile")
    ORGANIZATION = "organization", _("Verified organization")
    MODERATOR = "moderator", _("Moderator")
    SUPPORT = "support", _("Support")
    ADMIN = "admin", _("Administrator")


class Language(models.TextChoices):
    UZ_LATN = "uz", _("O'zbekcha (lotin)")
    UZ_CYRL = "uz-cyrl", _("Ўзбекча (кирилл)")
    RU = "ru", _("Русский")


def avatar_upload_to(instance: User, filename: str) -> str:
    return f"avatars/{instance.pk or 'new'}/{filename}"


class UserManager(BaseUserManager["User"]):
    use_in_migrations = True

    def create_user(self, phone: str, name: str = "", password: str | None = None, **extra):
        if not phone:
            raise ValueError("Users must have a phone number")
        user = self.model(phone=phone, name=name, **extra)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone: str, name: str = "", password: str | None = None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("role", Role.ADMIN)
        extra.setdefault("is_verified", True)
        if not extra["is_staff"] or not extra["is_superuser"]:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True")
        return self.create_user(phone, name=name, password=password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(_("phone"), max_length=20, unique=True)
    name = models.CharField(_("name"), max_length=40, blank=True)
    avatar = models.ImageField(_("avatar"), upload_to=avatar_upload_to, null=True, blank=True)
    city = models.ForeignKey(
        "catalog.City",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
        verbose_name=_("city"),
    )
    about = models.CharField(_("about"), max_length=200, blank=True)
    language = models.CharField(
        _("language"), max_length=10, choices=Language.choices, default=Language.UZ_LATN
    )
    # Phone is hidden by default; shown on a listing only if the owner opts in (§18.2).
    show_phone = models.BooleanField(_("show phone publicly"), default=False)

    role = models.CharField(_("role"), max_length=20, choices=Role.choices, default=Role.USER)
    is_verified = models.BooleanField(_("phone verified"), default=False)
    is_blocked = models.BooleanField(_("blocked"), default=False)
    block_reason = models.CharField(_("block reason"), max_length=255, blank=True)

    rating_avg = models.DecimalField(_("rating average"), max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(_("rating count"), default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    # Account deletion (§18.2): row kept but anonymized; is_active flips to False.
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-date_joined",)

    def __str__(self) -> str:
        return self.name or self.phone

    @property
    def is_new_account(self) -> bool:
        """Accounts younger than 7 days get extra limits (§18.6, §18.10)."""
        return (timezone.now() - self.date_joined).days < 7


class PhoneOTP(TimeStampedModel):
    """One-time SMS code for a phone number (§18.1). The code is stored hashed."""

    phone = models.CharField(_("phone"), max_length=20, db_index=True)
    code_hash = models.CharField(_("code hash"), max_length=128)
    expires_at = models.DateTimeField(_("expires at"))
    attempts = models.PositiveSmallIntegerField(_("wrong attempts"), default=0)
    locked_until = models.DateTimeField(_("locked until"), null=True, blank=True)
    consumed_at = models.DateTimeField(_("consumed at"), null=True, blank=True)

    class Meta:
        verbose_name = _("phone code")
        verbose_name_plural = _("phone codes")
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["phone", "created_at"])]

    def __str__(self) -> str:
        return f"OTP({self.phone})"

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_consumed(self) -> bool:
        return self.consumed_at is not None

    @property
    def is_locked(self) -> bool:
        return self.locked_until is not None and timezone.now() < self.locked_until


class Platform(models.TextChoices):
    IOS = "ios", "iOS"
    ANDROID = "android", "Android"
    WEB = "web", "Web"


class Device(TimeStampedModel):
    """A user's device for push notifications (§12 devices)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="devices"
    )
    fcm_token = models.CharField(_("FCM token"), max_length=255, unique=True)
    platform = models.CharField(_("platform"), max_length=10, choices=Platform.choices)
    app_version = models.CharField(_("app version"), max_length=20, blank=True)
    last_seen = models.DateTimeField(_("last seen"), default=timezone.now)

    class Meta:
        verbose_name = _("device")
        verbose_name_plural = _("devices")
        ordering = ("-last_seen",)

    def __str__(self) -> str:
        return f"{self.platform} / {self.user_id}"


class Session(TimeStampedModel):
    """A refresh-token session, labelled by device, for per-device revocation (§18.1).

    `jti` links to the SimpleJWT refresh token so logout can blacklist exactly one device.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions"
    )
    jti = models.CharField(_("token id"), max_length=64, unique=True)
    platform = models.CharField(_("platform"), max_length=10, choices=Platform.choices, blank=True)
    app_version = models.CharField(_("app version"), max_length=20, blank=True)
    user_agent = models.CharField(_("user agent"), max_length=255, blank=True)
    ip = models.GenericIPAddressField(_("IP"), null=True, blank=True)
    expires_at = models.DateTimeField(_("expires at"))
    revoked_at = models.DateTimeField(_("revoked at"), null=True, blank=True)

    class Meta:
        verbose_name = _("session")
        verbose_name_plural = _("sessions")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Session({self.user_id}, {self.platform})"
