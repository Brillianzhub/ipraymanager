from . import views
from django.urls import path


urlpatterns = [
    path('artists/', views.list_artists,
         name='artists'),
    path('song_list/', views.paginated_music, name='song-list'),
    path('by_artist/<id>/', views.songs_by_artist, name='song-by-artist'),
    path('top_trending/', views.top_trending, name='top-trending'),
    path('search/', views.search_music, name='search-music'),
    path('category/<category>/', views.songs_by_category, name='song-by-category'),
    path('increment_view/<int:pk>/', views.increment_music_views,
         name='increment-music-views'),
    path('<int:pk>/details/', views.get_music_with_related, name="music-details"),
]
