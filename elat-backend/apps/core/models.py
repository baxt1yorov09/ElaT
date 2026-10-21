"""Shared base models and mixins used across all apps.

- TimeStampedModel: created_at / updated_at on every row (SPEC §12).
- SoftDeleteModel: soft delete via deleted_at; default manager hides deleted rows.
- AuditLog: record of admin/moderator actions (SPEC §10.4, §14.1).
- RuntimeConfig: admin-editable overrides for SPEC §18 numeric limits.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self) -> "SoftDeleteQuerySet":
        return self.filter(deleted_at__isnull=True)

    def dead(self) -> "SoftDeleteQuerySet":
        return self.filter(deleted_at__isnull=False)

    def delete(self):  # type: ignore[override]
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()


class AliveManager(models.Manager):
    """Default manager: only rows that are not soft-deleted."""

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class AllManager(models.Manager):
    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteModel(TimeStampedModel):
    deleted_at = models.DateTimeField(null=True, blank=True, default=None, editable=False)

    objects = AliveManager()
    all_objects = AllManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):  # type: ignore[override]
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self) -> None:
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])


class AuditLog(TimeStampedModel):
    """Append-only log of privileged actions."""

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
    )
    action = models.CharField(_("action"), max_length=100)
    object_type = models.CharField(_("object type"), max_length=100, blank=True)
    object_id = models.CharField(_("object id"), max_length=64, blank=True)
    ip = models.GenericIPAddressField(_("IP"), null=True, blank=True)
    data = models.JSONField(_("data"), default=dict, blank=True)

    class Meta:
        verbose_name = _("audit log")
        verbose_name_plural = _("audit logs")
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["action", "created_at"])]

    def __str__(self) -> str:
        return f"{self.action} @ {self.created_at:%Y-%m-%d %H:%M}"


class RuntimeConfig(TimeStampedModel):
    """Runtime override for a SPEC §18 limit. Absent key => settings.ELAT_LIMITS default."""

    key = models.CharField(_("key"), max_length=100, unique=True)
    value = models.IntegerField(_("value"))
    description = models.CharField(_("description"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("runtime config")
        verbose_name_plural = _("runtime config")
        ordering = ("key",)

    def __str__(self) -> str:
        return f"{self.key}={self.value}"
