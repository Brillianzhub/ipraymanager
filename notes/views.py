# notes/views.py
from .serializers import NoteSyncCheckSerializer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Note
from .serializers import NoteSyncSerializer, NotePullSerializer
from django.utils.dateparse import parse_datetime
import uuid


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils.dateparse import parse_datetime
from .models import Note
from .serializers import NoteSyncSerializer
import uuid


# class NoteSyncView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         notes_data = request.data.get('notes', [])

#         synced_ids = []
#         errors = []

#         for data in notes_data:
#             note_id = data.get('id')
#             if not note_id:
#                 errors.append({"error": "Missing note ID", "data": data})
#                 continue

#             try:
#                 uuid.UUID(note_id)
#             except ValueError:
#                 errors.append({"error": "Invalid UUID format", "id": note_id})
#                 continue

#             incoming_client_modified = parse_datetime(
#                 data.get('last_modified'))

#             if not incoming_client_modified:
#                 errors.append(
#                     {"id": note_id, "error": "Invalid or missing last_modified timestamp"})
#                 continue

#             try:
#                 # Try to update an existing note
#                 note = Note.objects.get(id=note_id, user=user)

#                 if not note.client_last_modified or incoming_client_modified > note.client_last_modified:
#                     serializer = NoteSyncSerializer(
#                         note, data=data, partial=True)
#                     if serializer.is_valid():
#                         note = serializer.save()
#                         note.client_last_modified = incoming_client_modified
#                         note.save(update_fields=['client_last_modified'])
#                         synced_ids.append(str(note_id))
#                     else:
#                         errors.append(
#                             {"id": note_id, "errors": serializer.errors})
#                 else:
#                     synced_ids.append(str(note_id))

#             except Note.DoesNotExist:
#                 data_with_user = data.copy()
#                 data_with_user['user'] = user.id

#                 serializer = NoteSyncSerializer(data=data_with_user)
#                 if serializer.is_valid():
#                     note = serializer.save()
#                     note.client_last_modified = incoming_client_modified
#                     note.save(update_fields=['client_last_modified'])
#                     synced_ids.append(str(note_id))
#                 else:
#                     errors.append({"id": note_id, "errors": serializer.errors})

#         return Response({
#             "synced_ids": synced_ids,
#             "errors": errors
#         }, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import uuid
from .models import Note
from .serializers import NoteSyncSerializer


class NoteSyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        notes_data = request.data.get('notes', [])

        synced_ids = []
        errors = []

        for data in notes_data:
            note_id = data.get('id')
            if not note_id:
                errors.append({"error": "Missing note ID", "data": data})
                continue

            try:
                uuid.UUID(note_id)
            except ValueError:
                errors.append({"error": "Invalid UUID format", "id": note_id})
                continue

            client_modified = data.get('last_modified')
            if not client_modified:
                errors.append({
                    "id": note_id,
                    "error": "Missing last_modified timestamp"
                })
                continue

            try:
                # Try updating existing note
                note = Note.objects.get(id=note_id, user=user)
                serializer = NoteSyncSerializer(note, data=data, partial=True)
                if serializer.is_valid():
                    note = serializer.save()
                    note.client_last_modified = client_modified  # Raw string
                    note.save(update_fields=['client_last_modified'])
                    synced_ids.append(str(note_id))
                else:
                    errors.append({"id": note_id, "errors": serializer.errors})

            except Note.DoesNotExist:
                # Create a new note with user
                data_with_user = data.copy()
                data_with_user['user'] = user.id
                serializer = NoteSyncSerializer(data=data_with_user)
                if serializer.is_valid():
                    note = serializer.save()
                    note.client_last_modified = client_modified
                    note.save(update_fields=['client_last_modified'])
                    synced_ids.append(str(note_id))
                else:
                    errors.append({"id": note_id, "errors": serializer.errors})

        return Response({
            "synced_ids": synced_ids,
            "errors": errors
        }, status=status.HTTP_200_OK)


class NotePullView(APIView):
    """Fetch all notes for comparison/merging"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(
            user=request.user).order_by('-last_modified')
        serializer = NotePullSerializer(notes, many=True)
        return Response({
            "notes": serializer.data,
            "server_time": timezone.now().isoformat()
        })


class NoteBatchPullView(APIView):
    """Fetch specific notes by IDs"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        note_ids = request.data.get('note_ids', [])
        if not isinstance(note_ids, list):
            return Response({"error": "note_ids must be a list."}, status=status.HTTP_400_BAD_REQUEST)

        notes = Note.objects.filter(user=request.user, id__in=note_ids)
        serializer = NotePullSerializer(notes, many=True)
        return Response({"notes": serializer.data})


class NoteSyncCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(
            user=request.user
        ).only('id', 'client_last_modified', 'is_deleted')

        serializer = NoteSyncCheckSerializer(notes, many=True)

        return Response({
            "notes_meta": serializer.data,
            "server_time": timezone.now().isoformat()
        })
