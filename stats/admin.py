# stats/admin.py
from django.contrib import admin
from .models import FeatureClickAggregate


@admin.register(FeatureClickAggregate)
class FeatureClickAggregateAdmin(admin.ModelAdmin):
    list_display = ("feature", "date", "count")
    list_filter = ("feature", "date")
    ordering = ("-date", "-count")
    search_fields = ("feature",)
