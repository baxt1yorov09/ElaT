from __future__ import annotations

import pytest
from django.core.management import call_command

from apps.catalog.models import Category, CategoryAttribute, City, District


@pytest.mark.django_db
def test_seed_catalog_is_idempotent() -> None:
    call_command("seed_catalog")
    cities = City.objects.count()
    categories = Category.objects.count()

    # Toshkent is the pilot city with districts seeded.
    toshkent = City.objects.get(name_uz="Toshkent")
    assert toshkent.districts.count() >= 5

    # Car and property attribute schemas exist.
    assert CategoryAttribute.objects.filter(category__slug="avtomobil", key="year").exists()
    assert CategoryAttribute.objects.filter(category__slug="kvartira", key="rooms").exists()

    # Running again does not duplicate rows.
    call_command("seed_catalog")
    assert City.objects.count() == cities
    assert Category.objects.count() == categories
    assert District.objects.filter(city=toshkent).count() >= 5
