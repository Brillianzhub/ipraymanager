from django.urls import path
from . import views

urlpatterns = [
    path('collections/', views.get_sermons, name='get_sermons'),
    path('categories/', views.get_categories, name='get_categories'),
    path('videos/<int:video_id>/increment-views/',
         views.increment_video_views, name='increment-video-views'),
    path('total-stats/', views.total_counts, name='total-stats'),
]
