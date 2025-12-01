from .models import YouTubeVideo
from .models import Month, DailyReading, DailyFamilyDevotional, Year
from rest_framework import serializers


# class DailyFamilyDevotionalSerializer(serializers.ModelSerializer):
#     reflectionQuestions = serializers.SerializerMethodField()
#     title = serializers.CharField(source="title.theme")
#     theme = serializers.CharField(source="theme.title")

#     class Meta:
#         model = DailyFamilyDevotional
#         fields = [
#             'id',
#             'title',
#             'theme',
#             'bible_verse_text',
#             'bible_verse_reference',
#             'devotion',
#             'reflectionQuestions',
#             'prayer',
#             'family_challenge',
#             'devotional_date',
#             'date_created',
#         ]

#     def get_reflectionQuestions(self, obj):
#         questions = filter(None, [
#             obj.reflection_question_1,
#             obj.reflection_question_2,
#             obj.reflection_question_3
#         ])
#         return list(questions)

class DailyFamilyDevotionalSerializer(serializers.ModelSerializer):
    monthly_theme = serializers.CharField(source='title.theme', read_only=True)
    daily_theme = serializers.CharField(source='theme.title', read_only=True)

    class Meta:
        model = DailyFamilyDevotional
        fields = [
            'id', 'devotional_date', 'monthly_theme', 'daily_theme',
            'bible_verse_text', 'bible_verse_reference', 'devotion',
            'reflection_question_1', 'reflection_question_2', 'reflection_question_3',
            'prayer', 'family_challenge'
        ]


class DailyReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReading
        fields = ["date", "title", "scripture"]

    from rest_framework import serializers


class YouTubeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = ["id", "title", "url", "description", "published_at"]


class MonthSerializer(serializers.ModelSerializer):
    daily_readings = DailyReadingSerializer(many=True, read_only=True)
    videos = YouTubeVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Month
        fields = ["id", "name", "theme", "daily_readings", "videos"]


class YearSerializer(serializers.ModelSerializer):
    months = MonthSerializer(many=True, read_only=True)

    class Meta:
        model = Year
        fields = ["year", "theme", "months"]
