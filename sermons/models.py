from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    video_count = models.PositiveIntegerField(default=0)  # Counter for videos

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="videos")
    url = models.URLField(unique=True)
    source = models.CharField(
        max_length=255, blank=True, null=True)
    preacher = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    date_published = models.DateField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_published']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.category.video_count = self.category.videos.count()
            self.category.save()

    def delete(self, *args, **kwargs):
        category = self.category
        super().delete(*args, **kwargs)
        category.video_count = category.videos.count()
        category.save()
