"""Catalog: cities, districts, category tree and category attribute schemas (SPEC §12).

Section codes match listings.section: gift (Saxovat), sale (Savdo), flea (Baraholka),
swap (Almashtirish), need (Menga kerak). A category lists which sections it applies to.
"""

from __future__ import annotations

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Section(models.TextChoices):
    GIFT = "gift", _("Saxovat")
    SALE = "sale", _("Savdo")
    FLEA = "flea", _("Baraholka")
    SWAP = "swap", _("Almashtirish")
    NEED = "need", _("Menga kerak")


class AttributeType(models.TextChoices):
    STRING = "string", _("Text")
    INTEGER = "integer", _("Integer")
    DECIMAL = "decimal", _("Decimal")
    BOOLEAN = "boolean", _("Boolean")
    CHOICE = "choice", _("Single choice")


class City(TimeStampedModel):
    name_uz = models.CharField(_("name (uz-Latn)"), max_length=100)
    name_uz_cyrl = models.CharField(_("name (uz-Cyrl)"), max_length=100, blank=True)
    name_ru = models.CharField(_("name (ru)"), max_length=100, blank=True)
    center = gis_models.PointField(_("center"), geography=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")
        ordering = ("order", "name_uz")

    def __str__(self) -> str:
        return self.name_uz


class District(TimeStampedModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="districts")
    name_uz = models.CharField(_("name (uz-Latn)"), max_length=100)
    name_uz_cyrl = models.CharField(_("name (uz-Cyrl)"), max_length=100, blank=True)
    name_ru = models.CharField(_("name (ru)"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("district")
        verbose_name_plural = _("districts")
        ordering = ("name_uz",)
        unique_together = ("city", "name_uz")

    def __str__(self) -> str:
        return f"{self.city.name_uz} / {self.name_uz}"


class Category(TimeStampedModel):
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    slug = models.SlugField(_("slug"), max_length=80, unique=True)
    name_uz = models.CharField(_("name (uz-Latn)"), max_length=100)
    name_uz_cyrl = models.CharField(_("name (uz-Cyrl)"), max_length=100, blank=True)
    name_ru = models.CharField(_("name (ru)"), max_length=100, blank=True)
    icon = models.CharField(_("icon"), max_length=50, blank=True)
    sections = models.JSONField(
        _("sections"),
        default=list,
        help_text=_("Section codes this category applies to, e.g. ['sale', 'gift']."),
    )
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ("order", "name_uz")
        indexes = [models.Index(fields=["parent", "order"])]

    def __str__(self) -> str:
        return self.name_uz


class CategoryAttribute(TimeStampedModel):
    """Category-specific field (e.g. car: year, mileage, fuel; property: rooms, area)."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="attributes")
    key = models.CharField(_("key"), max_length=50)
    type = models.CharField(_("type"), max_length=10, choices=AttributeType.choices)
    label_uz = models.CharField(_("label (uz-Latn)"), max_length=100)
    label_uz_cyrl = models.CharField(_("label (uz-Cyrl)"), max_length=100, blank=True)
    label_ru = models.CharField(_("label (ru)"), max_length=100, blank=True)
    options = models.JSONField(_("options"), default=list, blank=True)
    required = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _("category attribute")
        verbose_name_plural = _("category attributes")
        ordering = ("category", "order")
        unique_together = ("category", "key")

    def __str__(self) -> str:
        return f"{self.category.slug}.{self.key}"
