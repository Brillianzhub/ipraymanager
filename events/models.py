from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Title of the event"
    )
    description = models.TextField(
        max_length=500,
        help_text="Brief description of the event"
    )

    start_date = models.DateTimeField(
        help_text="When the event starts"
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Optional: when the event ends"
    )
    website_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Link to more information or registration"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events_created'
    )

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title
