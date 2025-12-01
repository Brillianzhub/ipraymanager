from django.contrib import admin
from .models import ServiceReview


@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "rate",
        "city",
        "country",
        "agreed_to_publish",  # show consent in the list
        "publish",
        "created_at"
    )
    list_filter = ("publish", "rate", "country", "created_at")
    search_fields = ("full_name", "review", "city", "country")
    ordering = ("-created_at",)
    actions = ["publish_reviews", "unpublish_reviews"]

    # Make agreed_to_publish readonly in the admin detail view
    readonly_fields = ["agreed_to_publish"]

    def publish_reviews(self, request, queryset):
        updated = queryset.update(publish=True)
        self.message_user(request, f"{updated} review(s) published.")
    publish_reviews.short_description = "Publish selected reviews"

    def unpublish_reviews(self, request, queryset):
        updated = queryset.update(publish=False)
        self.message_user(request, f"{updated} review(s) unpublished.")
    unpublish_reviews.short_description = "Unpublish selected reviews"
