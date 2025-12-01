from django.contrib import admin
from .models import ShareTemplate


@admin.register(ShareTemplate)
class TemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for Template model
    """
    list_display = [
        'name',
        'template_type',
        'text_color',
        'background',
        'created_at',
        'updated_at'
    ]

    list_filter = [
        'template_type',
        'created_at',
        'updated_at'
    ]

    search_fields = [
        'name',
        'template_type'
    ]

    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'template_type']
        }),
        ('Colors & Background', {
            'fields': ['gradient_colors', 'background', 'text_color']
        }),
        ('Styles', {
            'fields': ['styles'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
