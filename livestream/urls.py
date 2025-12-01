from django.urls import path
from .views import CurrentLiveStreamView, LiveStreamDetailView, CurrentLiveStatusView, LiveStreamView, LiveStreamLightView, LiveStreamIncrementView

urlpatterns = [
    path("list/", LiveStreamView.as_view(), name="livestream-view-list"),
    path("listing/", LiveStreamLightView.as_view(), name="livestream-view-listing"),
    path("item/", CurrentLiveStreamView.as_view(), name="livestream-list"),
    path("<int:pk>/", LiveStreamDetailView.as_view(),
         name="livestream-detail"),
    path("status/", CurrentLiveStatusView.as_view(),
         name="livestream-status"),
    path("livestream/<int:pk>/increment-view/", LiveStreamIncrementView.as_view(),
          name="livestream-increment-view"
),

]
