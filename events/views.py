from django.utils import timezone
from rest_framework import viewsets, permissions
from .models import Event
from .serializers import EventSerializer
from django.db.models import Q


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        now = timezone.now()
        base_qs = Event.objects.all().order_by('-start_date')

        if self.action == 'list':
            return base_qs.filter(
                is_active=True
            ).filter(
                Q(end_date__isnull=True) | Q(end_date__gte=now)
            )
        return base_qs  # For retrieve, update, delete

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
