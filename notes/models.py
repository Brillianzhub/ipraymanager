import uuid
from django.db import models
from accounts.models import User


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=100)
    date = models.DateTimeField()
    tags = models.JSONField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)

    client_last_modified = models.TextField(null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['date'], name='idx_notes_date'),
            models.Index(fields=['is_favorite'], name='idx_notes_favorite'),
            models.Index(fields=['is_deleted'], name='idx_notes_deleted'),
        ]
        ordering = ['-date']
