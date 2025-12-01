# notes/admin.py
from django.contrib import admin
from .models import Note


# @admin.register(Note)
# class NoteAdmin(admin.ModelAdmin):
#     list_display = ('title', 'user', 'category',
#                     'is_favorite', 'date', 'last_modified')
#     list_filter = ('category', 'is_favorite', 'date')
#     search_fields = ('title', 'content', 'tags')
#     ordering = ('-date',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date')
    list_filter = ('category', 'is_favorite')
    search_fields = ('title', 'content')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filter out any potentially corrupt records
        return qs.exclude(id__isnull=True)
