# stats/urls.py
from django.urls import path
from .views import FeatureClickBulkCreateView, FeatureClickStatsView

urlpatterns = [
    path("click/", FeatureClickBulkCreateView.as_view(), name="feature-click-bulk"),
    path("feature-clicks/", FeatureClickStatsView.as_view(),
         name="feature-click-stats"),
]
