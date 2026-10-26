"""SMS auth + profile tests (SPEC §18.1, §18.2)."""

from __future__ import annotations

import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from apps.users.models import PhoneOTP, Session, User
from apps.users.tests.factories import UserFactory

SEND_URL = "/api/v1/auth/sms/send"
VERIFY_URL = "/api/v1/auth/sms/verify"
ME_URL = "/api/v1/users/me"

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def fixed_code(monkeypatch):
    monkeypatch.setattr("apps.users.services._generate_code", lambda: "123456")
    return "123456"


@pytest.fixture
def client() -> APIClient:
    return APIClient()


# --- phone validation -------------------------------------------------------
def test_send_rejects_bad_phone(client):
    resp = client.post(SEND_URL, {"phone": "+99812345"}, format="json")
    assert resp.status_code == 400
    assert resp.data["code"] == "invalid_phone"


def test_send_normalizes_and_creates_otp(client, fixed_code):
    resp = client.post(SEND_URL, {"phone": "+998 90 123 45 67"}, format="json")
    assert resp.status_code == 200
    assert resp.data["phone"] == "+998901234567"
    assert PhoneOTP.objects.filter(phone="+998901234567").count() == 1


def test_resend_cooldown(client, fixed_code):
    client.post(SEND_URL, {"phone": "+998901112233"}, format="json")
    resp = client.post(SEND_URL, {"phone": "+998901112233"}, format="json")
    assert resp.status_code == 429
    assert resp.data["code"] == "resend_too_soon"


# --- verify -----------------------------------------------------------------
def test_verify_success_issues_tokens_and_creates_user(client, fixed_code):
    phone = "+998901234567"
    client.post(SEND_URL, {"phone": phone}, format="json")
    resp = client.post(VERIFY_URL, {"phone": phone, "code": fixed_code}, format="json")
    assert resp.status_code == 200
    assert resp.data["access"] and resp.data["refresh"]
    assert resp.data["is_new"] is True
    assert resp.data["user"]["phone"] == phone
    user = User.objects.get(phone=phone)
    assert user.is_verified is True
    assert Session.objects.filter(user=user).count() == 1


def test_verify_wrong_code_counts_down_then_locks(client, fixed_code):
    phone = "+998901234567"
    client.post(SEND_URL, {"phone": phone}, format="json")
    # 4 wrong attempts keep returning invalid_code with a remaining count.
    for _ in range(4):
        resp = client.post(VERIFY_URL, {"phone": phone, "code": "000000"}, format="json")
        assert resp.status_code == 400
        assert resp.data["code"] == "invalid_code"
    # 5th wrong attempt locks the phone.
    resp = client.post(VERIFY_URL, {"phone": phone, "code": "000000"}, format="json")
    assert resp.status_code == 429
    assert resp.data["code"] == "too_many_attempts"
    # Even the correct code is now refused while locked.
    resp = client.post(VERIFY_URL, {"phone": phone, "code": fixed_code}, format="json")
    assert resp.status_code == 429


def test_verify_expired_code(client, fixed_code):
    phone = "+998901234567"
    client.post(SEND_URL, {"phone": phone}, format="json")
    otp = PhoneOTP.objects.get(phone=phone)
    from django.utils import timezone

    otp.expires_at = timezone.now() - timezone.timedelta(seconds=1)
    otp.save(update_fields=["expires_at"])
    resp = client.post(VERIFY_URL, {"phone": phone, "code": fixed_code}, format="json")
    assert resp.status_code == 400
    assert resp.data["code"] == "code_expired"


def test_blocked_user_cannot_request_code(client, fixed_code):
    UserFactory(phone="+998901234567", is_blocked=True, block_reason="spam")
    resp = client.post(SEND_URL, {"phone": "+998901234567"}, format="json")
    assert resp.status_code == 403
    assert resp.data["code"] == "account_blocked"


# --- profile ----------------------------------------------------------------
def test_me_requires_auth(client):
    assert client.get(ME_URL).status_code == 401


def test_profile_update_and_name_validation(client):
    user = UserFactory()
    client.force_authenticate(user)

    ok = client.patch(ME_URL, {"name": "Ali Valiyev", "about": "Salom"}, format="json")
    assert ok.status_code == 200
    assert ok.data["name"] == "Ali Valiyev"

    bad = client.patch(ME_URL, {"name": "A"}, format="json")
    assert bad.status_code == 400

    bad_link = client.patch(ME_URL, {"name": "www.spam.uz"}, format="json")
    assert bad_link.status_code == 400


def test_account_deletion_anonymizes(client, fixed_code):
    user = UserFactory(phone="+998901234567")
    client.force_authenticate(user)
    # A fresh code is needed to confirm deletion.
    client.post(SEND_URL, {"phone": user.phone}, format="json")
    resp = client.post("/api/v1/users/me/delete", {"code": fixed_code}, format="json")
    assert resp.status_code == 204
    user.refresh_from_db()
    assert user.is_active is False
    assert user.deleted_at is not None
    assert user.name == ""
    assert user.phone.startswith("deleted-")
