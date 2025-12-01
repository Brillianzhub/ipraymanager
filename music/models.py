from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(upload_to="artists/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    active_from = models.DateField(
        blank=True, null=True)

    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube_channel = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MusicCategory(models.TextChoices):
    HYMN = "HYMN", "Hymn"
    WORSHIP = "WORSHIP", "Worship"
    PRAISE = "PRAISE", "Praise"
    GOSPEL = "GOSPEL", "Gospel"
    CHORAL = "CHORAL", "Choral"
    OTHER = "OTHER", "Other"


class Music(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist,
        related_name="songs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    url = models.URLField(unique=True)
    category = models.CharField(
        max_length=20,
        choices=MusicCategory.choices,
        default=MusicCategory.WORSHIP
    )

    views = models.PositiveIntegerField(default=0)

    date_published = models.DateField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    featured = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def youtube_id(self):
        import re
        match = re.search(r'(?:v=|youtu\.be/)([^&]+)', self.url)
        return match.group(1) if match else None

    @property
    def thumbnail(self):
        if self.youtube_id:
            return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"
        return None
