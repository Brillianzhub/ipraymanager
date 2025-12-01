import hashlib
from django.db import models
from django.utils.text import slugify


class Preacher(models.Model):
    name = models.CharField(max_length=255)
    ministry = models.CharField(max_length=255, blank=True, null=True)
    photo = models.URLField(max_length=500, blank=True, null=True)
    sermon_count = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.ministry})" if self.ministry else self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    video_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class VideoManager(models.Manager):
    def most_viewed(self, limit=10):
        return self.order_by('-views')[:limit]


class Video(models.Model):
    title = models.CharField(max_length=255)
    content_id = models.CharField(
        max_length=64, unique=True, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="videos")
    url = models.URLField(unique=True)
    source = models.CharField(
        max_length=255, blank=True, null=True)
    preacher = models.ForeignKey(
        Preacher,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="videos"
    )
    description = models.TextField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    date_published = models.DateField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)

    objects = VideoManager()

    class Meta:
        ordering = ["-date_published", "-date_added"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_category = None
        old_preacher = None

        if not self.content_id:
            # Use a deterministic hash if possible
            base_str = f"{self.title}|{self.preacher_id}|{self.date_published}"
            full_hash = hashlib.sha256(base_str.encode("utf-8")).hexdigest()
            self.content_id = full_hash[:16]

        if not is_new:
            # Check if category or preacher changed
            old = Video.objects.get(pk=self.pk)
            if old.category != self.category:
                old_category = old.category
            if old.preacher != self.preacher:
                old_preacher = old.preacher

        super().save(*args, **kwargs)

        # Update current category count
        self.category.video_count = self.category.videos.count()
        self.category.save()

        # Update preacher count
        self.preacher.sermon_count = self.preacher.videos.count()
        self.preacher.save()

        # If category or preacher changed, update the old ones
        if old_category:
            old_category.video_count = old_category.videos.count()
            old_category.save()

        if old_preacher:
            old_preacher.sermon_count = old_preacher.videos.count()
            old_preacher.save()

    def delete(self, *args, **kwargs):
        category = self.category
        preacher = self.preacher
        super().delete(*args, **kwargs)

        # Update counters after deletion
        category.video_count = category.videos.count()
        category.save()

        preacher.sermon_count = preacher.videos.count()
        preacher.save()
