from __future__ import annotations

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.core.config import clear_limit_cache, get_limit
from apps.core.models import AuditLog, RuntimeConfig
from apps.core.services import log_action


@pytest.fixture
def api() -> APIClient:
    return APIClient()


def test_ping_is_public(api: APIClient) -> None:
    resp = api.get("/api/v1/ping")
    assert resp.status_code == 200
    assert resp.json() == {"pong": True}


def test_error_format_is_code_message_details(api: APIClient) -> None:
    # A DRF-handled error (wrong method on ping) returns the unified envelope.
    resp = api.post("/api/v1/ping")
    assert resp.status_code == 405
    body = resp.json()
    assert set(body.keys()) == {"code", "message", "details"}
    assert body["code"] == "method_not_allowed"


@pytest.mark.django_db
def test_get_limit_prefers_runtime_config() -> None:
    clear_limit_cache("listing_images_max")
    assert get_limit("listing_images_max") == 10  # settings default
    RuntimeConfig.objects.create(key="listing_images_max", value=7)
    clear_limit_cache("listing_images_max")
    assert get_limit("listing_images_max") == 7


def test_get_limit_unknown_key_raises() -> None:
    with pytest.raises(KeyError):
        get_limit("nope_not_a_limit")


@pytest.mark.django_db
def test_log_action_writes_audit_row(django_user_model) -> None:
    user = django_user_model.objects.create(phone="+998901234567", name="Test")
    entry = log_action(actor=user, action="listing.approve", obj=user, ip="127.0.0.1")
    assert AuditLog.objects.count() == 1
    assert entry.object_type == "User"
    assert entry.actor == user


@pytest.mark.django_db
def test_healthz_ok(api: APIClient) -> None:
    resp = api.get(reverse("healthz"))
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
