from django.db import models
from django.utils import timezone
from datetime import date
from django.core.cache import cache


class Year(models.Model):
    year = models.PositiveIntegerField(unique=True, default=date.today().year)
    theme = models.TextField()

    def __str__(self):
        return str(self.year)


class Month(models.Model):
    year = models.ForeignKey(
        Year,
        on_delete=models.CASCADE,
        related_name="months",
        default=None,
        null=True
    )
    name = models.CharField(max_length=100, unique=True)
    theme = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.year.year if self.year else 'No Year'}) - {self.theme}"


class DailyReading(models.Model):
    month = models.ForeignKey(
        Month, on_delete=models.CASCADE, related_name="daily_readings")
    date = models.DateField(unique=True)
    title = models.CharField(max_length=200)
    scripture = models.CharField(max_length=100)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.date} - {self.title} ({self.scripture})"


class DailyFamilyDevotional(models.Model):
    title = models.ForeignKey(
        Month, on_delete=models.CASCADE, related_name="monthly_theme")
    theme = models.ForeignKey(
        DailyReading, on_delete=models.CASCADE, related_name="daily_theme")
    bible_verse_text = models.TextField()
    bible_verse_reference = models.CharField(max_length=255)
    devotion = models.TextField()
    reflection_question_1 = models.TextField(null=True, blank=True)
    reflection_question_2 = models.TextField(null=True, blank=True)
    reflection_question_3 = models.TextField(null=True, blank=True)
    prayer = models.TextField()
    family_challenge = models.TextField(null=True, blank=True)
    devotional_date = models.DateField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-devotional_date']
        verbose_name = 'Daily Family Devotional'
        verbose_name_plural = 'Daily Family Devotionals'
        indexes = [
            models.Index(fields=['devotional_date']),
        ]

    def __str__(self):
        return f"{self.theme} - {self.devotional_date}"

    def get_next_devotional(self):
        return DailyFamilyDevotional.objects.filter(
            devotional_date__gt=self.devotional_date
        ).order_by('devotional_date').first()

    def get_previous_devotional(self):
        return DailyFamilyDevotional.objects.filter(
            devotional_date__lt=self.devotional_date
        ).order_by('-devotional_date').first()

    @classmethod
    def get_devotional_by_date(cls, search_date):
        cache_key = f"devotional_{search_date}"
        devotional = cache.get(cache_key)

        if devotional is None:
            devotional = (
                cls.objects
                # Preload Month and DailyReading
                .select_related("title", "theme")
                .only(
                    "id", "devotional_date", "date_created",
                    "bible_verse_text", "bible_verse_reference",
                    "devotion", "prayer", "family_challenge",
                    "reflection_question_1", "reflection_question_2", "reflection_question_3",
                    "title__theme",  
                    "theme__title",  
                )
                .filter(devotional_date=search_date)
                .first()
            )

            if devotional:
                cache.set(cache_key, devotional,
                          timeout=60 * 60)  # Cache 1 hour

        return devotional

    @classmethod
    def get_today_devotional(cls):
        today = timezone.now().date()
        return cls.get_devotional_by_date(today)


class YouTubeVideo(models.Model):
    monthly_devotion = models.ForeignKey(
        Month, related_name="videos", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
