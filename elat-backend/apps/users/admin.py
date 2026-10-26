from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import Device, PhoneOTP, Session, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("-date_joined",)
    list_display = ("phone", "name", "role", "is_verified", "is_blocked", "is_staff")
    list_filter = ("role", "is_verified", "is_blocked", "is_staff", "is_active")
    search_fields = ("phone", "name")

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Profile"), {"fields": ("name", "avatar", "city", "about", "language", "show_phone")}),
        (
            _("Status"),
            {"fields": ("role", "is_verified", "is_blocked", "block_reason", "is_active")},
        ),
        (_("Rating"), {"fields": ("rating_avg", "rating_count")}),
        (_("Permissions"), {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Dates"), {"fields": ("last_login", "date_joined", "last_seen", "deleted_at")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("phone", "name", "password1", "password2")}),
    )
    readonly_fields = (
        "date_joined",
        "last_login",
        "last_seen",
        "deleted_at",
        "rating_avg",
        "rating_count",
    )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "platform", "app_version", "last_seen")
    list_filter = ("platform",)
    search_fields = ("user__phone", "fcm_token")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("user", "platform", "created_at", "expires_at", "revoked_at")
    list_filter = ("platform",)
    search_fields = ("user__phone", "jti")
    readonly_fields = ("jti",)


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ("phone", "created_at", "expires_at", "attempts", "locked_until", "consumed_at")
    search_fields = ("phone",)
    readonly_fields = ("code_hash",)
