from django.urls import path
from . import views

urlpatterns = [
    path('register-token/', views.register_token, name='register_token'),
    path('unregister-token/', views.delete_token, name='delete_token'),

    path('send-general-notification/', views.send_general_notification_view,
         name='send-general-notification'),

    path('email-notifications/toggle/', views.toggle_email_notifications,
         name='toggle_email_notifications'),
    path('email-notifications/unsubscribe/', views.unsubscribe_email_notifications,
         name='unsubscribe_email_notifications'),

    path('email-notifications/send/', views.send_email_to_subscribed_users,
         name='send_email_to_subscribed_users')
]
