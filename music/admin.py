from django.contrib import admin
from .models import Artist, Music


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'active_from', 'date_added')
    search_fields = ('name', 'country')
    list_filter = ('country', 'active_from')
    ordering = ('name',)
    readonly_fields = ('date_added',)

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "photo", "bio", "country")
        }),
        ("Career Info", {
            "fields": ("active_from", "date_of_birth")
        }),
        ("Social & Contact", {
            "fields": ("facebook", "instagram", "youtube_channel", "website")
        }),
        ("System", {
            "fields": ("date_added",),
        }),
    )


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'views',
                    'featured', 'recommended', 'date_added')
    list_filter = ('category', 'featured', 'recommended')
    search_fields = ('title', 'artist__name')
    ordering = ('-views',)
    readonly_fields = ('date_added', 'views')

    fieldsets = (
        ("Music Info", {
            "fields": ("title", "artist", "url", "category", "duration", "lyrics")
        }),
        ("Status & Highlights", {
            "fields": ("views", "featured", "recommended")
        }),
        ("Timeline", {
            "fields": ("date_published", "date_added")
        }),
    )
