import re
from bibles.models import VerseKJV
from rest_framework import serializers
from .models import Prayer


class PrayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prayer
        fields = ['id', 'prayer_category',
                  'prayer', 'prayer_scripture', 'publish', 'featured', 'last_updated']


class PrayerWithScriptureContentSerializer(serializers.ModelSerializer):
    scripture_text = serializers.SerializerMethodField()

    class Meta:
        model = Prayer
        fields = [
            'id',
            'prayer_category',
            'prayer',
            'prayer_scripture',
            'scripture_text',
            'publish',
            'featured',
            'last_updated',
        ]

    def get_scripture_text(self, obj):
        """
        Supports:
        - Single verse: "John 3:16"
        - Verse range: "John 3:16-18"
        - Multiple refs: "John 3:16; Romans 8:28"
        - Multi-word books: "1 Kings 3:5", "Song of Solomon 2:4"
        """
        if not obj.prayer_scripture:
            return None

        results = []
        refs = [ref.strip() for ref in obj.prayer_scripture.split(";")]

        for ref in refs:
            # Match "BookName Chapter:Verse[-EndVerse]"
            match = re.match(
                r'([\d]?\s?[A-Za-z\s]+)\s+(\d+):(\d+)(?:-(\d+))?', ref)
            if not match:
                continue

            book_name, chapter_number, start_verse, end_verse = match.groups()
            chapter_number = int(chapter_number)
            start_verse = int(start_verse)
            end_verse = int(end_verse) if end_verse else start_verse

            verses = VerseKJV.objects.filter(
                chapter__book__name__iexact=book_name.strip(),
                chapter__number=chapter_number,
                verse__gte=start_verse,
                verse__lte=end_verse,
            ).order_by("verse")

            verse_texts = [v.text for v in verses]
            if verse_texts:
                results.append(" ".join(verse_texts))

        return " ".join(results) if results else None

# class PrayerWithScriptureContentSerializer(serializers.ModelSerializer):
#     scripture_text = serializers.SerializerMethodField()

#     class Meta:
#         model = Prayer
#         fields = [
#             'id',
#             'prayer_category',
#             'prayer',
#             'prayer_scripture',
#             'scripture_text',
#             'publish',
#             'featured',
#             'last_updated',
#         ]

#     def get_scripture_text(self, obj):
#         """
#         Parse prayer_scripture (e.g. 'John 3:16') and fetch text from VerseKJV.
#         Currently supports single verse references.
#         """
#         if not obj.prayer_scripture:
#             return None

#         try:
#             # Example: "John 3:16"
#             match = re.match(
#                 r'([\d]?\s?[A-Za-z]+)\s+(\d+):(\d+)', obj.prayer_scripture)
#             if not match:
#                 return None

#             book_name, chapter_number, verse_number = match.groups()

#             verse_obj = VerseKJV.objects.select_related('chapter__book').get(
#                 chapter__book__name__iexact=book_name.strip(),
#                 chapter__number=int(chapter_number),
#                 verse=int(verse_number),
#             )
#             return verse_obj.text

#         except VerseKJV.DoesNotExist:
#             return None
#         except Exception as e:
#             return None  # Or str(e) for debugging
