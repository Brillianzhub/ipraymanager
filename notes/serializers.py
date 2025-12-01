from rest_framework import serializers
from .models import Note


class NotePullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'category',
                  'date', 'tags', 'is_favorite', 'last_modified', 'client_last_modified']


class NoteSyncSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose')

    class Meta:
        model = Note
        fields = '__all__'


class NoteSyncCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'client_last_modified', 'is_deleted']
