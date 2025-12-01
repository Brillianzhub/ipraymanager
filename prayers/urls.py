# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.get_all_prayers, name='prayer-list'),
    path('create/', views.create_prayer, name='create_prayer'),
    path('meta/', views.prayers_meta, name='prayer-meta'),
    path('by-scripture/', views.get_prayers_by_scripture,
         name='prayers-by-scripture'),
    path("prayers-with-scripture/",
         views.PrayerWithScriptureAPIView.as_view(), name="prayers-website"),
    path("categories/", views.get_prayer_categories,
         name="prayer-categories"),
    path("featured/", views.get_featured_prayers, name="featured-prayers"),
]
