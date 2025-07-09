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

    # Optional: Hide expired events from admin unless explicitly filtered
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.GET.get('end_date__isnull') is None and request.GET.get('end_date__gte') is None:
            now = timezone.now()
            return qs.filter(end_date__isnull=True) | qs.filter(end_date__gte=now)
        return qs
