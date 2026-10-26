from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsNotBlocked(BasePermission):
    """Authenticated and not blocked (§18.1 blocked-user rule)."""

    message = _("Akkauntingiz bloklangan")

    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(user and user.is_authenticated and not user.is_blocked)
