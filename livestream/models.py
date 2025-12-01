from django.db import models


class LiveStream(models.Model):
    title = models.CharField(max_length=255)
    preacher = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    youtube_video_id = models.CharField(
        max_length=50, help_text="YouTube video/stream ID")
    is_live = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    viewer_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, blank=True)
    thumbnail = models.URLField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return f"{self.title} ({'LIVE' if self.is_live else 'Scheduled'})"
