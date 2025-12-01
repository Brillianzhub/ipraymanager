from django.db import models


class Prayer(models.Model):
    prayer_category = models.CharField(max_length=100)
    prayer = models.TextField()
    prayer_scripture = models.CharField(max_length=255, blank=True)
    featured = models.BooleanField(default=False)
    publish = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_updated']

    def __str__(self):
        return f"{self.prayer_category.title()} Prayer"
