from __future__ import annotations

from django.contrib import admin

from apps.catalog.models import Category, CategoryAttribute, City, District


class DistrictInline(admin.TabularInline):
    model = District
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "name_ru", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("name_uz", "name_ru")
    inlines = [DistrictInline]


class CategoryAttributeInline(admin.TabularInline):
    model = CategoryAttribute
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "slug", "parent", "sections", "is_active", "order")
    list_filter = ("is_active", "parent")
    list_editable = ("is_active", "order")
    search_fields = ("name_uz", "name_ru", "slug")
    prepopulated_fields = {"slug": ("name_uz",)}
    inlines = [CategoryAttributeInline]


@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):
    list_display = ("category", "key", "type", "required", "order")
    list_filter = ("type", "required")
    search_fields = ("key", "category__slug")
