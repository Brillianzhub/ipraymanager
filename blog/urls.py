from django.urls import path
from . import views

urlpatterns = [
    path("fetch/", views.fetch_blogs, name="fetch_blogs"),
    path("categories/", views.get_categories, name="get-categories"),
    path("fetch/<slug:slug>/", views.fetch_blog, name="fetch_blog"),
    path("create/", views.create_blog, name="create_blog"),
    path("update/<slug:slug>/", views.update_blog, name="update_blog"),
    path("delete/<slug:slug>/", views.delete_blog, name="delete_blog"),
    path("toggle/<slug:slug>/", views.toggle_publish, name="toggle_publish"),
]
