from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'website_link',
            'created_at',
            'is_active',
            'created_by',
        ]
        read_only_fields = ['id', 'created_at', 'created_by']
