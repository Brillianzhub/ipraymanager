from django.db import models


class FeatureClickAggregate(models.Model):
    FEATURE_CHOICES = [
        ("hymns", "Hymns"),
        ("devotion", "Devotion"),
        ("sermons", "Sermons"),
        ("bible", "Bible"),
        ("prayer", "Prayer"),
        ("notes", "Notes"),
    ]
    feature = models.CharField(
        max_length=20, choices=FEATURE_CHOICES)
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("feature", "date")
