from django.contrib import admin
from .models import DailyFamilyDevotional
from .models import Month,  DailyReading

from .models import Year

from django.contrib import admin
from .models import YouTubeVideo


class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "monthly_devotion", "url", "published_at")
    search_fields = ("title", " monthly_devotion__name")
    list_filter = ("published_at",)
    ordering = ("-published_at",)


admin.site.register(YouTubeVideo, YouTubeVideoAdmin)


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    search_fields = ('year',)
    ordering = ('year',)


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ("name", "theme")
    search_fields = ("name", "theme")


@admin.register(DailyReading)
class DailyReadingAdmin(admin.ModelAdmin):
    list_display = ("date", "title", "scripture")
    search_fields = ("date", "title", "scripture")


@admin.register(DailyFamilyDevotional)
class DailyFamilyDevotionalAdmin(admin.ModelAdmin):
    list_display = ('theme', 'devotional_date', 'date_created')
    list_filter = ('devotional_date', 'date_created')
    search_fields = ('theme', 'bible_verse_reference',
                     'devotion')
    ordering = ('-devotional_date',)
    date_hierarchy = 'devotional_date'

    readonly_fields = ('date_created',)

    fieldsets = (
        (None, {
            'fields': ('title', 'theme', 'devotional_date')
        }),
        ('Bible Verse', {
            'fields': ('bible_verse_text', 'bible_verse_reference')
        }),
        ('Devotion Content', {
            'fields': ('devotion',)
        }),
        ('Reflection Questions', {
            'fields': ('reflection_question_1', 'reflection_question_2', 'reflection_question_3')
        }),
        ('Prayer & Challenge', {
            'fields': ('prayer', 'family_challenge')
        }),
        ('Metadata', {
            'fields': ('date_created',)
        }),
    )
