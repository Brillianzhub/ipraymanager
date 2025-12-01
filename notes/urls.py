from django.urls import path
from .views import NoteSyncView, NotePullView,  NoteSyncCheckView, NoteBatchPullView

urlpatterns = [
    path('sync/', NoteSyncView.as_view(), name='note-sync'),
    path('pull/', NotePullView.as_view(), name='note-pull'),
    path('sync-check/', NoteSyncCheckView.as_view(), name='note-sync-check'),
    path('fetch-specific/', NoteBatchPullView.as_view(), name='fetch-specific'),
]
