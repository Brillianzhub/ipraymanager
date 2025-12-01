from django.urls import path
from . import views

urlpatterns = [
    path('collections/', views.get_sermons, name='get_sermons'),
    path('categories/', views.get_categories, name='get_categories'),
    path('videos/<int:video_id>/increment-views/',
         views.increment_video_views, name='increment-video-views'),
    path('total-stats/', views.total_counts, name='total-stats'),

    # New Endpoints
    path("preachers/", views.PreacherListView.as_view(), name="preacher-list"),
    path("preachers/<int:preacher_id>/categories/",
         views.PreacherCategoryListView.as_view(), name="preacher-categories"),
    path("preachers/<int:preacher_id>/categories/<int:category_id>/videos/",
         views.PreacherCategoryVideoListView.as_view(), name="preacher-category-videos"),
    path("videos/<int:id>/", views.VideoDetailView.as_view(), name="video-detail"),
    path('featured-sermons/', views.featured_sermons, name='featured-sermons'),
    path('recommended-sermons/', views.recommended_sermons,
         name='recommended-sermons'),
    path('top-sermons/', views.most_viewed_sermons,
         name='top-sermons')
]
