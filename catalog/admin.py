from django.contrib import admin
from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "purchase_price", "category", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("category",)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "version_number", "version_name", "is_current")
    search_fields = ("product", "version_name")
    list_filter = ("product",)
