from django.urls import path
from .views import RegisterView, VerifyEmailView, ResendVerificationView
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-token/', ResendVerificationView.as_view(), name='resend-token'),
    path('login/', views.CustomLoginView.as_view(), name='custom-token-login'),
    path("login/apple/", views.AppleLoginView.as_view(), name="apple-login"),
    path('me/', views.MeView.as_view(), name='me'),
    path('password-reset/request/', views.PasswordResetRequestView.as_view(),
         name='password-reset-request'),
    path('password-reset/verify/', views.PasswordResetVerifyView.as_view(),
         name='password-reset-verify'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('logout/', views.logout_view, name='logout'),
    path('facebook/login-url/', views.facebook_login_url,
         name='facebook_login_url'),


    path("facebook/callback/",
         views.facebook_callback, name="facebook_callback"),
    #     path('token-login/', obtain_auth_token, name='token-login'),

    path("facebook/stats/", views.facebook_page_stats),
]
