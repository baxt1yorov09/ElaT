"""Custom phone-based user.

Defined in Phase 0 on purpose: AUTH_USER_MODEL must be set before the first migration
(Django pitfall). Phase 1 extends this with SMS auth, device sessions, badges, rating, etc.
Passwords are not used for normal users (SMS login); staff/superusers keep passwords for admin.
"""

from __future__ import annotations

from typing import ClassVar

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    GUEST = "guest", _("Guest")
    USER = "user", _("User")
    BUSINESS = "business", _("Business profile")
    ORGANIZATION = "organization", _("Verified organization")
    MODERATOR = "moderator", _("Moderator")
    SUPPORT = "support", _("Support")
    ADMIN = "admin", _("Administrator")


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
    language = models.CharField(_("language"), max_length=10, default="uz")

    role = models.CharField(_("role"), max_length=20, choices=Role.choices, default=Role.USER)
    is_verified = models.BooleanField(_("phone verified"), default=False)
    is_blocked = models.BooleanField(_("blocked"), default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-date_joined",)

    def __str__(self) -> str:
        return self.name or self.phone
