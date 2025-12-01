from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('notes/', include('notes.urls')),
    path('sermons/', include('sermons.urls')),
    path('devotion/', include('devotion.urls')),
    path('events/', include('events.urls')),
    path('prayers/', include('prayers.urls')),
    path('hymns/', include('hymns.urls')),
    path('notifications/', include('notifications.urls')),
    path('sharetemplates/', include('sharetemplates.urls')),
    path('livestream/', include('livestream.urls')),
    path('bibles/', include('bibles.urls')),
    path('chat/', include('chat.urls')),
    path('stats/', include('stats.urls')),
]
