from django.contrib import admin
from .models import Category, Video


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'preacher',
                    'source', 'date_published')
    list_filter = ('category', 'source', 'date_published')
    search_fields = ('title', 'preacher', 'source', 'url')
