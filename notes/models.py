# models.py
from accounts.models import User
from django.db import models


class Note(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_notes')
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=100)
    date = models.DateTimeField()
    tags = models.JSONField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.email}"
