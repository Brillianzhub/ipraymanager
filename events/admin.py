from django.contrib import admin
from django.utils import timezone
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'start_date',
        'end_date',
        'is_active',
        'is_expired',
        'created_by',
        'created_at',
    )
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-start_date',)

    def is_expired(self, obj):
        return obj.end_date and obj.end_date < timezone.now()
    is_expired.boolean = True
    is_expired.short_description = 'Expired?'
