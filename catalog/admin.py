from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "owner",
        "is_published",
        "price",
        "updated_at",
    )
    list_filter = ("category", "is_published")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("category", "owner")
    ordering = ("-updated_at",)