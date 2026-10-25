"""Seed cities, districts, the category tree and category attribute schemas.

Idempotent: safe to run repeatedly (uses update_or_create / get_or_create).
Pilot city is Toshkent (DECISIONS D2); more cities are added via this command or admin.

Usage: python manage.py seed_catalog
"""

from __future__ import annotations

from typing import Any

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalog.models import AttributeType, Category, CategoryAttribute, City, District, Section

CITIES: list[dict[str, Any]] = [
    {
        "name_uz": "Toshkent",
        "name_uz_cyrl": "Тошкент",
        "name_ru": "Ташкент",
        "center": Point(69.2401, 41.2995),
        "order": 0,
        "districts": [
            ("Chilonzor", "Чилонзор", "Чиланзар"),
            ("Yunusobod", "Юнусобод", "Юнусабад"),
            ("Mirzo Ulug'bek", "Мирзо Улуғбек", "Мирзо-Улугбек"),
            ("Shayxontohur", "Шайхонтоҳур", "Шайхантахур"),
            ("Yakkasaroy", "Яккасарой", "Яккасарай"),
            ("Sergeli", "Сергели", "Сергели"),
        ],
    },
    {
        "name_uz": "Samarqand",
        "name_uz_cyrl": "Самарқанд",
        "name_ru": "Самарканд",
        "center": Point(66.9597, 39.6542),
        "order": 1,
        "districts": [],
    },
    {
        "name_uz": "Namangan",
        "name_uz_cyrl": "Наманган",
        "name_ru": "Наманган",
        "center": Point(71.6726, 40.9983),
        "order": 2,
        "districts": [],
    },
]

ALL = [Section.GIFT, Section.SALE, Section.FLEA, Section.SWAP, Section.NEED]

# (slug, uz, cyrl, ru, icon, sections, [children])
CATEGORIES: list[tuple] = [
    (
        "mebel",
        "Mebel",
        "Мебел",
        "Мебель",
        "sofa",
        ALL,
        [
            ("divan", "Divan", "Диван", "Диван", "", ALL, []),
            ("stol-stul", "Stol va stul", "Стол ва стул", "Столы и стулья", "", ALL, []),
        ],
    ),
    (
        "texnika",
        "Texnika",
        "Техника",
        "Техника",
        "tv",
        ALL,
        [
            ("telefon", "Telefon", "Телефон", "Телефоны", "smartphone", ALL, []),
            (
                "maishiy-texnika",
                "Maishiy texnika",
                "Маиший техника",
                "Бытовая техника",
                "",
                ALL,
                [],
            ),
        ],
    ),
    ("kiyim", "Kiyim", "Кийим", "Одежда", "shirt", ALL, []),
    ("kitoblar", "Kitoblar", "Китоблар", "Книги", "book", ALL, []),
    ("bolalar", "Bolalar", "Болалар", "Детские товары", "baby", ALL, []),
    (
        "transport",
        "Transport",
        "Транспорт",
        "Транспорт",
        "car",
        [Section.SALE, Section.SWAP],
        [
            (
                "avtomobil",
                "Avtomobil",
                "Автомобил",
                "Автомобили",
                "car",
                [Section.SALE, Section.SWAP],
                [],
            ),
        ],
    ),
    (
        "kochmas-mulk",
        "Ko'chmas mulk",
        "Кўчмас мулк",
        "Недвижимость",
        "home",
        [Section.SALE],
        [
            ("kvartira", "Kvartira", "Квартира", "Квартиры", "home", [Section.SALE], []),
        ],
    ),
    ("antikvar", "Antikvar", "Антиквар", "Антиквариат", "gem", [Section.FLEA], []),
]

# Category attribute schemas (SPEC §18.3): car and property extra fields.
ATTRIBUTES: dict[str, list[dict[str, Any]]] = {
    "avtomobil": [
        {
            "key": "year",
            "type": AttributeType.INTEGER,
            "label_uz": "Yil",
            "label_uz_cyrl": "Йил",
            "label_ru": "Год",
            "required": True,
            "order": 0,
        },
        {
            "key": "mileage",
            "type": AttributeType.INTEGER,
            "label_uz": "Probeg (km)",
            "label_uz_cyrl": "Пробег (км)",
            "label_ru": "Пробег (км)",
            "required": False,
            "order": 1,
        },
        {
            "key": "fuel",
            "type": AttributeType.CHOICE,
            "label_uz": "Yoqilg'i",
            "label_uz_cyrl": "Ёқилғи",
            "label_ru": "Топливо",
            "required": False,
            "order": 2,
            "options": ["benzin", "dizel", "gaz", "elektr", "gibrid"],
        },
    ],
    "kvartira": [
        {
            "key": "rooms",
            "type": AttributeType.INTEGER,
            "label_uz": "Xonalar soni",
            "label_uz_cyrl": "Хоналар сони",
            "label_ru": "Количество комнат",
            "required": True,
            "order": 0,
        },
        {
            "key": "area",
            "type": AttributeType.DECIMAL,
            "label_uz": "Maydon (m²)",
            "label_uz_cyrl": "Майдон (m²)",
            "label_ru": "Площадь (m²)",
            "required": False,
            "order": 1,
        },
    ],
}


class Command(BaseCommand):
    help = "Seed cities, districts, categories and category attributes."

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        self._seed_cities()
        self._seed_categories()
        self.stdout.write(self.style.SUCCESS("Catalog seeded."))

    def _seed_cities(self) -> None:
        for c in CITIES:
            districts = c.pop("districts", [])
            city, _created = City.objects.update_or_create(
                name_uz=c["name_uz"],
                defaults={k: v for k, v in c.items() if k != "name_uz"},
            )
            for uz, cyrl, ru in districts:
                District.objects.update_or_create(
                    city=city,
                    name_uz=uz,
                    defaults={"name_uz_cyrl": cyrl, "name_ru": ru},
                )
        self.stdout.write(
            f"  cities: {City.objects.count()}, districts: {District.objects.count()}"
        )

    def _seed_categories(self) -> None:
        for order, (slug, uz, cyrl, ru, icon, sections, children) in enumerate(CATEGORIES):
            parent = self._upsert_category(slug, uz, cyrl, ru, icon, sections, order, None)
            for child_order, child in enumerate(children):
                cslug, cuz, ccyrl, cru, cicon, csections, _ = child
                self._upsert_category(cslug, cuz, ccyrl, cru, cicon, csections, child_order, parent)
        self._seed_attributes()
        self.stdout.write(
            f"  categories: {Category.objects.count()}, "
            f"attributes: {CategoryAttribute.objects.count()}"
        )

    def _upsert_category(self, slug, uz, cyrl, ru, icon, sections, order, parent) -> Category:
        category, _created = Category.objects.update_or_create(
            slug=slug,
            defaults={
                "name_uz": uz,
                "name_uz_cyrl": cyrl,
                "name_ru": ru,
                "icon": icon,
                "sections": [s.value for s in sections],
                "order": order,
                "parent": parent,
            },
        )
        return category

    def _seed_attributes(self) -> None:
        for slug, attrs in ATTRIBUTES.items():
            try:
                category = Category.objects.get(slug=slug)
            except Category.DoesNotExist:
                continue
            for attr in attrs:
                CategoryAttribute.objects.update_or_create(
                    category=category,
                    key=attr["key"],
                    defaults={
                        "type": attr["type"],
                        "label_uz": attr["label_uz"],
                        "label_uz_cyrl": attr["label_uz_cyrl"],
                        "label_ru": attr["label_ru"],
                        "options": attr.get("options", []),
                        "required": attr.get("required", False),
                        "order": attr.get("order", 0),
                    },
                )
