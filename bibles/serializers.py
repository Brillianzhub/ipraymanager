# serializers.py
from rest_framework import serializers

class VerseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    verse = serializers.IntegerField()
    text = serializers.CharField()
