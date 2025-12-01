from django.urls import path
from .views import ContactCreateView, ContactListView, ContactDetailView

urlpatterns = [
    path("submit/", ContactCreateView.as_view(), name="contact-create"),
    path("fetch/", ContactListView.as_view(), name="contact-list"),
    path("fetch/<int:pk>/",
         ContactDetailView.as_view(), name="contact-detail"),
]
