from rest_framework import serializers
from .models import LiveStream


class LiveStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStream
        fields = "__all__"  



class CurrentLiveStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStream
        fields = ["id", "title", "is_live"]


class LiveStreamLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStream
        fields = [
            "id",
            "title",
            "preacher",
            "thumbnail",
            "youtube_video_id",
            "category",
            "is_live"
        ]
