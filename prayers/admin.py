from django.contrib import admin
from .models import Prayer


@admin.register(Prayer)
class PrayerAdmin(admin.ModelAdmin):
    list_display = ('prayer_category', 'featured')
    list_filter = ('prayer_category', 'featured')
    search_fields = ('prayer', 'prayer_scripture')
