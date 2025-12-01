from django.db import models


class Hymn(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    has_chorus = models.BooleanField(default=False)
    chorus = models.TextField(blank=True, null=True)
    scripture_references = models.TextField(
        blank=True, null=True, help_text="Comma-separated or JSON list of scripture references")
    copyright = models.CharField(
        max_length=255, default="Public domain")  # new
    source = models.CharField(max_length=255, default="hymnary.org")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Stanza(models.Model):
    hymn = models.ForeignKey(
        Hymn, related_name='stanzas', on_delete=models.CASCADE)
    stanza_number = models.PositiveIntegerField()
    text = models.TextField()

    class Meta:
        unique_together = ('hymn', 'stanza_number')
        ordering = ['stanza_number']

    def __str__(self):
        return f"Stanza {self.stanza_number} of '{self.hymn.title}'"
