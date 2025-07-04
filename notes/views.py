# notes/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer


class NotesBackupAPIView(APIView):
    def post(self, request):
        serializer = NoteSerializer(
            data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Notes backed up successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
