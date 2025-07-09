from rest_framework import serializers
from .models import Video, Category


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'category', 'url',
            'source', 'preacher', 'description',
            'date_published', 'date_added', 'views'
        ]


class CategorySerializer(serializers.ModelSerializer):
    # videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'video_count', 'description']
