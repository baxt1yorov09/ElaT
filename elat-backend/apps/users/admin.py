from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("-date_joined",)
    list_display = ("phone", "name", "role", "is_verified", "is_blocked", "is_staff")
    list_filter = ("role", "is_verified", "is_blocked", "is_staff", "is_active")
    search_fields = ("phone", "name")

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Profile"), {"fields": ("name", "language")}),
        (_("Status"), {"fields": ("role", "is_verified", "is_blocked", "is_active")}),
        (_("Permissions"), {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Dates"), {"fields": ("last_login", "date_joined", "last_seen")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("phone", "name", "password1", "password2")}),
    )
    readonly_fields = ("date_joined", "last_login", "last_seen")
