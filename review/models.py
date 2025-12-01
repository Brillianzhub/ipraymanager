from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ServiceReview(models.Model):
    RATE_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1–5 stars

    rate = models.PositiveSmallIntegerField(
        choices=RATE_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating scale: 1 (worst) - 5 (best)"
    )
    review = models.TextField(help_text="User's review of the app")
    full_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    agreed_to_publish = models.BooleanField(
        default=False,
        help_text="User agrees that their review may be published on the website and app"
    )

    publish = models.BooleanField(
        default=False,
        help_text="Mark as published to show on website"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.rate}⭐ ({'Published' if self.publish else 'Unpublished'})"
