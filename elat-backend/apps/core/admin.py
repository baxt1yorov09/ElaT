from __future__ import annotations

from django.contrib import admin

from apps.core.config import clear_limit_cache
from apps.core.models import AuditLog, RuntimeConfig


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "actor", "object_type", "object_id", "ip", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("action", "object_type", "object_id")
    readonly_fields = ("actor", "action", "object_type", "object_id", "ip", "data", "created_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(RuntimeConfig)
class RuntimeConfigAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "description", "updated_at")
    search_fields = ("key", "description")

    def save_model(self, request, obj, form, change) -> None:
        super().save_model(request, obj, form, change)
        clear_limit_cache(obj.key)

    def delete_model(self, request, obj) -> None:
        key = obj.key
        super().delete_model(request, obj)
        clear_limit_cache(key)
