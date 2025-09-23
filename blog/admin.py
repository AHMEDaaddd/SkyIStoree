from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_published", "views", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
