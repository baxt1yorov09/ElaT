from __future__ import annotations

from typing import Any

from apps.core.models import AuditLog


def log_action(
    *,
    actor: Any = None,
    action: str,
    obj: Any = None,
    ip: str | None = None,
    data: dict[str, Any] | None = None,
) -> AuditLog:
    """Record a privileged action in the audit log (SPEC §10.4)."""
    object_type = ""
    object_id = ""
    if obj is not None:
        object_type = obj.__class__.__name__
        object_id = str(getattr(obj, "pk", "") or "")
    return AuditLog.objects.create(
        actor=actor if getattr(actor, "pk", None) else None,
        action=action,
        object_type=object_type,
        object_id=object_id,
        ip=ip,
        data=data or {},
    )
