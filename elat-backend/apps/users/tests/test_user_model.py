from __future__ import annotations

import pytest

from apps.users.models import Role, User


@pytest.mark.django_db
def test_create_user_has_unusable_password() -> None:
    user = User.objects.create_user(phone="+998901112233", name="Dilnoza")
    assert user.pk is not None
    assert user.role == Role.USER
    assert not user.has_usable_password()
    assert str(user) == "Dilnoza"


@pytest.mark.django_db
def test_create_superuser_is_admin() -> None:
    admin = User.objects.create_superuser(phone="+998900000000", password="x")
    assert admin.is_staff and admin.is_superuser
    assert admin.role == Role.ADMIN
    assert admin.is_verified


@pytest.mark.django_db
def test_str_falls_back_to_phone() -> None:
    user = User.objects.create_user(phone="+998901234567")
    assert str(user) == "+998901234567"
