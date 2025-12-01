from django.urls import path
from .views import get_chapter_verses

urlpatterns = [
    path("<str:version>/<str:book_name>/<int:chapter_number>/", get_chapter_verses),
]
