from rest_framework import serializers
from .models import ServiceReview


class ServiceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReview
        fields = [
            "id",
            "rate",
            "review",
            "full_name",
            "city",
            "country",
            "agreed_to_publish",  
            "publish",
            "created_at"
        ]
        # publish is now writable by admin
        read_only_fields = ["id", "created_at"]

    def validate_agreed_to_publish(self, value):
        """
        Ensure that the user agrees to have their review published.
        """
        # Only enforce this if this is a user-submitted review (not admin editing)
        request = self.context.get("request")
        if request and request.method in ["POST"] and not value:
            raise serializers.ValidationError(
                "You must agree to have your review published."
            )
        return value
