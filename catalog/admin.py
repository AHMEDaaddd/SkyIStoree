from django.contrib import admin
from .models import Category, Product, Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "phone", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        list_display = ("id", "name", "is_published", "created_at")
        list_filter = ("is_published",)
        search_fields = ("name", "description")
        prepopulated_fields = {"slug": ("name",)}