from rest_framework import generics, permissions
from .models import ServiceReview
from .serializers import ServiceReviewSerializer


class ServiceReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Only published reviews are visible
        return ServiceReview.objects.filter(publish=True).order_by("-created_at")


class ServiceReviewAdminListView(generics.ListAPIView):
    """
    Admin-only endpoint to fetch all reviews (published + unpublished).
    """
    queryset = ServiceReview.objects.all().order_by("-created_at")
    serializer_class = ServiceReviewSerializer
    permission_classes = [permissions.IsAdminUser]


class ServiceReviewAdminDetailView(generics.RetrieveUpdateAPIView):
    """
    Admin-only endpoint to retrieve and update a review
    (e.g., mark publish/unpublish, edit text).
    """
    queryset = ServiceReview.objects.all()
    serializer_class = ServiceReviewSerializer
    permission_classes = [permissions.IsAdminUser]
