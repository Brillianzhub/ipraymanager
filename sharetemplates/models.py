
import json
from django.contrib.auth.models import User
from django.db import models


class TemplateTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ShareTemplate(models.Model):
    """
    Template model for storing prayer and Bible verse template definitions
    """
    TEMPLATE_TYPE_CHOICES = [
        ('verse', 'Bible Verse'),
        ('prayer', 'Prayer'),
        ('quote', 'Quote'),
        ('hymn', 'Hymn'),
        ('devotion', 'Devotion'),
    ]

    name = models.CharField(
        max_length=100,
        help_text="Template name (e.g., 'Heavenly Light')"
    )

    template_type = models.CharField(
        max_length=10,
        choices=TEMPLATE_TYPE_CHOICES,
        help_text="Type of template"
    )

    gradient_colors = models.JSONField(
        help_text="List of hex/rgb colors for gradient background",
        default=list
    )

    background = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Optional fallback background color (hex code)"
    )

    text_color = models.CharField(
        max_length=20,
        help_text="Text color (hex code)"
    )

    styles = models.JSONField(
        help_text="Style definitions (lightRay1, verseText, referenceBadge, etc.)",
        default=dict
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Template"
        verbose_name_plural = "Templates"

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

    def clean(self):
        """Validate the model data"""
        from django.core.exceptions import ValidationError

        # Validate gradient_colors is a list
        if not isinstance(self.gradient_colors, list):
            raise ValidationError(
                {'gradient_colors': 'Must be a list of colors'})

        # Validate styles is a dict
        if not isinstance(self.styles, dict):
            raise ValidationError(
                {'styles': 'Must be a dictionary of style definitions'})

        # Validate color format (basic hex validation)
        if self.text_color and not self.text_color.startswith('#'):
            if len(self.text_color) not in [6, 7]:
                raise ValidationError(
                    {'text_color': 'Must be a valid hex color code'})

        if self.background and not self.background.startswith('#'):
            if len(self.background) not in [6, 7]:
                raise ValidationError(
                    {'background': 'Must be a valid hex color code'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
