from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status
from .models import EmailNotification
from accounts.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ipraymanager.utils import send_general_notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Device
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def register_token(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        body = json.loads(request.body)
        token = body.get('token')
        user_id = body.get('user_id')

        if not token:
            return JsonResponse({'error': 'Token is required'}, status=400)

        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

        existing_device = Device.objects.filter(token=token).first()
        if existing_device:
            if existing_device.user == user:
                return JsonResponse({'status': 'Token already registered'}, status=200)
            else:
                return JsonResponse({'error': 'Token is already associated with another user'}, status=409)

        Device.objects.create(token=token, user=user)
        return JsonResponse({'status': 'Token registered successfully'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred', 'details': str(e)}, status=500)


@csrf_exempt
def delete_token(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        token = body.get('token')

        if token:
            try:
                device = Device.objects.get(token=token)
                device.delete()
                return JsonResponse({'status': 'Token deleted successfully'}, status=200)
            except Device.DoesNotExist:
                return JsonResponse({'error': 'Token not found'}, status=404)
        else:
            return JsonResponse({'error': 'No token provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def send_general_notification_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        title = body.get('title')
        message = body.get('message')
        data = body.get('data', {})

        if not title or not message:
            return JsonResponse({'error': 'Title and message are required'}, status=400)

        return send_general_notification(title, message, data)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['POST'])
@permission_classes([AllowAny])
def toggle_email_notifications(request):
    if request.user.is_authenticated:
        notification, created = EmailNotification.objects.get_or_create(
            user=request.user
        )
    else:
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required for guest users.'},
                            status=status.HTTP_400_BAD_REQUEST)

        notification, created = EmailNotification.objects.get_or_create(
            email=email
        )

    if created:
        # First time subscribing → set to True
        notification.receive_email_notifications = True
    else:
        # Toggle current state
        notification.receive_email_notifications = not notification.receive_email_notifications

    notification.save()

    return Response({
        'message': 'Email notifications updated.',
        'subscribed': notification.receive_email_notifications
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def unsubscribe_email_notifications(request):
    email = request.query_params.get('email')

    if not email:
        return render(request, 'emails/unsubscribe_error.html', {
            'message': 'No email provided.'
        }, status=400)

    try:
        notification = EmailNotification.objects.get(email=email)
        notification.delete()
        return render(request, 'emails/unsubscribe_success.html', {
            'email': email
        })
    except EmailNotification.DoesNotExist:
        return render(request, 'emails/unsubscribe_error.html', {
            'message': 'We could not find an active subscription for this email.'
        }, status=404)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def send_email_to_subscribed_users(request):
    subject = request.data.get('subject')
    message = request.data.get('message')
    from_email = "IPray Daily <noreply@ipraydaily.net>"

    if not subject or not message:
        return Response({'error': 'Subject and message are required.'}, status=status.HTTP_400_BAD_REQUEST)

    subscribers = EmailNotification.objects.filter(
        receive_email_notifications=True).select_related('user')

    if not subscribers.exists():
        return Response({'message': 'No subscribers to email.'}, status=status.HTTP_204_NO_CONTENT)

    success_count = 0
    for subscriber in subscribers:
        if subscriber.user:
            last_name = getattr(subscriber.user, 'last_name',
                                '') or subscriber.user.last_name or 'Dear'
            email_address = subscriber.user.email
        else:
            last_name = 'there'
            email_address = subscriber.email

        # Build HTML email
        html_content = render_to_string(
            'emails/notification_email.html',
            {
                'last_name': last_name,
                'subject': subject,
                'unsubscribe_url': f"https://ipraymanager.com/notifications/email-notifications/unsubscribe/?email={email_address}",
                'message': message
            }
        )

        # Send the email
        email = EmailMultiAlternatives(
            subject, message, from_email, [email_address])
        email.attach_alternative(html_content, "text/html")
        email.send()
        success_count += 1

    return Response({'message': f'HTML email sent to {success_count} subscribers.'}, status=status.HTTP_200_OK)
