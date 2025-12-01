from django.conf import settings
from firebase_admin import credentials
import firebase_admin
from notifications.models import Device
from django.http import JsonResponse
import requests
import json


EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"


def send_push_notification(title, message, data=None, device_tokens=None, group_id=None):
    # Ensure device_tokens is provided
    if not device_tokens:
        return JsonResponse({'error': 'Device tokens are required'}, status=400)

    # Handle device_tokens as a list
    if isinstance(device_tokens, str):
        device_tokens = [device_tokens]

    notifications = []

    # Prepare individual notifications
    for token in device_tokens:
        notification = {
            "to": token,
            "title": title,
            "body": message,
            "data": data or {},
        }
        if group_id:
            notification["android"] = {
                "group": group_id,
            }
        notifications.append(notification)

    # Add a single group summary notification if group_id is provided
    if group_id:
        group_summary_notification = {
            "to": group_id,
            "title": f"{len(device_tokens)} new messages in Group Chat",
            "body": message,
            "data": {
                "groupId": f"group-{group_id}",
                **(data or {}),
            },
            "android": {
                "channelId": "group-chat",
                "isGroupSummary": True,
                "priority": "high",
            },
        }
        notifications.append(group_summary_notification)

    try:
        # Send notifications
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = requests.post(
            EXPO_PUSH_URL, headers=headers, data=json.dumps(notifications)
        )
        response_data = response.json()
        if response.status_code == 200:
            return JsonResponse({
                'status': 'Notifications sent successfully',
                'response': response_data,
                'total_notifications': len(notifications),
                'tokens_sent': [n['to'] for n in notifications],
            }, status=200)
        else:
            return JsonResponse({
                'error': 'Failed to send notifications',
                'status_code': response.status_code,
                'details': response_data,
            }, status=500)
    except requests.RequestException as e:
        return JsonResponse({
            'error': 'An error occurred while sending notifications',
            'details': str(e),
        }, status=500)


def send_general_notification(title, message, data=None):
    devices = Device.objects.all()

    if not devices.exists():
        return JsonResponse({'error': 'No devices found'}, status=404)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    notifications = []

    # Prepare notifications for all devices
    for device in devices:
        if device.token:
            notification = {
                "to": device.token,
                "title": title,
                "body": message,
                "data": data or {},
            }
            notifications.append(notification)

    try:
        # Send notifications
        response = requests.post(
            EXPO_PUSH_URL, headers=headers, data=json.dumps(notifications)
        )
        if response.status_code == 200:
            return JsonResponse({
                'status': 'Notifications sent successfully',
                'total_notifications': len(notifications),
                'tokens_sent': [n['to'] for n in notifications],
            }, status=200)
        else:
            return JsonResponse({
                'error': 'Failed to send notifications',
                'details': response.text,
            }, status=500)
    except requests.RequestException as e:
        return JsonResponse({
            'error': 'An error occurred while sending notifications',
            'details': str(e),
        }, status=500)


if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIAL)
    firebase_admin.initialize_app(cred)
