# hymns/urls.py

from django.urls import path
from .views import HymnListAPIView, HymnDetailAPIView

urlpatterns = [
    path('', HymnListAPIView.as_view(), name='hymn-list'),
    path('<int:id>/', HymnDetailAPIView.as_view(), name='hymn-detail'),
]
