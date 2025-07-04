from django.urls import path
from .views import RegisterView, VerifyEmailView, ResendVerificationView
from . import views


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-token/', ResendVerificationView.as_view(), name='resend-token'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('me/', views.MeView.as_view(), name='me'),
    path('password-reset/request/', views.PasswordResetRequestView.as_view(),
         name='password-reset-request'),
    path('password-reset/verify/', views.PasswordResetVerifyView.as_view(),
         name='password-reset-verify'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
