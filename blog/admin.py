from django.contrib import admin
from .models import Category, Blog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "category",
        "status",
        "featured",
        "publish",
        "last_updated",
    )
    list_filter = ("status", "featured", "category", "created", "last_updated")
    search_fields = ("title", "description", "body",
                     "author__username", "category__name")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    ordering = ("-publish",)
    raw_id_fields = ("author", "category")
    autocomplete_fields = ("tags",)
    readonly_fields = ("created", "last_updated",
                       "publish")  # ✅ mark as read-only

    fieldsets = (
        (None, {
            "fields": ("title", "slug", "description", "body", "image", "tags")
        }),
        ("Relations", {
            "fields": ("author", "category")
        }),
        ("Status & Metadata", {
            "fields": ("status", "featured", "read_time", "created", "last_updated", "publish")
        }),
    )
