from django.urls import path
from .views import (
    ServiceReviewListCreateView,
    ServiceReviewAdminListView,
    ServiceReviewAdminDetailView,
)

urlpatterns = [
    # Public
    path("", ServiceReviewListCreateView.as_view(), name="service-reviews"),

    # Admin
    path("admin/", ServiceReviewAdminListView.as_view(),
         name="admin-service-reviews"),
    path("admin/<int:pk>/", ServiceReviewAdminDetailView.as_view(),
         name="admin-service-review-detail"),
]
