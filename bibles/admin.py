from django.contrib import admin
from . models import Category, Book, Chapter,  VerseKJV, VerseASV, VerseAMP, VerseNIV

# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Chapter)


class VerseKJVAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ['text']


admin.site.register(VerseKJV, VerseKJVAdmin)
admin.site.register(VerseASV)
admin.site.register(VerseAMP)
admin.site.register(VerseNIV)
