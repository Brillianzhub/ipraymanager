# notes/urls.py
from django.urls import path
from .views import NotesBackupAPIView

urlpatterns = [
    path('backup/', NotesBackupAPIView.as_view(), name='notes-backup'),
]
