# events/admin.py
from django.contrib import admin
from .models import LiveStream


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "end_time", "is_live")
    list_filter = ("is_live", "start_time")
    search_fields = ("title", "description")
