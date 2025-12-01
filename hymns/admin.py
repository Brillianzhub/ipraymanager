from django.contrib import admin
from .models import Hymn, Stanza


class StanzaInline(admin.TabularInline):
    model = Stanza
    extra = 1  # Number of empty stanzas to display by default
    fields = ('stanza_number', 'text')
    ordering = ('stanza_number',)


@admin.register(Hymn)
class HymnAdmin(admin.ModelAdmin):
    list_display = ('title', 'has_chorus', 'copyright')
    search_fields = ('title',)
    inlines = [StanzaInline]
    ordering = ('title',)


@admin.register(Stanza)
class StanzaAdmin(admin.ModelAdmin):
    list_display = ('hymn', 'stanza_number')
    list_filter = ('hymn',)
    ordering = ('hymn', 'stanza_number')
