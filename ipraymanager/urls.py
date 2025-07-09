from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('notes/', include('notes.urls')),
    path('sermons/', include('sermons.urls'))
]
