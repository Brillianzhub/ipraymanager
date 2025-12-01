from django.utils import timezone
from rest_framework import viewsets, permissions
from .models import Event
from .serializers import EventSerializer
from django.db.models import Q


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        base_qs = Event.objects.all().order_by('-start_date')
        return base_qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Optional: Ensure only the creator can update
        event = self.get_object()
        if event.created_by != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not allowed to update this event.")
        serializer.save()

    def perform_destroy(self, instance):
        # Optional: Ensure only the creator can delete
        if instance.created_by != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not allowed to delete this event.")
        instance.delete()
