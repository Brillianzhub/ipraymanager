# notes/admin.py
from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'date', 'is_favorite')
    list_filter = ('category', 'is_favorite', 'date')
    search_fields = ('title', 'content', 'tags')
    ordering = ('-date',)
