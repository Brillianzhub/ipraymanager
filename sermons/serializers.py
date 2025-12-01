
from rest_framework import serializers
from .models import Preacher, Category, Video


class PreacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preacher
        fields = ['id', 'name', 'ministry',
                  'photo', 'sermon_count', 'featured']


class PreacherCategorySerializer(serializers.ModelSerializer):
    video_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'video_count']

    def get_video_count(self, obj):
        preacher_id = self.context.get('preacher_id')
        return obj.videos.filter(preacher_id=preacher_id).count()


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    preacher = serializers.CharField(source='preacher.name', read_only=True)

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'content_id', 'category', 'url',
            'source', 'preacher', 'description',
            'date_published', 'date_added', 'views'
        ]


class CategorySerializer(serializers.ModelSerializer):
    # videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'video_count', 'description']


class FeaturedVideoSerializer(serializers.ModelSerializer):
    preacher_name = serializers.CharField(
        source='preacher.name', read_only=True)
    preacher_ministry = serializers.CharField(
        source='preacher.ministry', read_only=True)
    category_name = serializers.CharField(
        source='category.name', read_only=True)

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'url',
            'preacher_name',
            'category_name',
            'preacher_ministry',
            'date_published',
            'description',
            'views'
        ]


class TopVideoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ['id', 'title', 'url']


class RecommendedVideoSerializer(serializers.ModelSerializer):
    preacher_name = serializers.CharField(
        source='preacher.name', read_only=True)
    preacher_ministry = serializers.CharField(
        source='preacher.ministry', read_only=True)
    category_name = serializers.CharField(
        source='category.name', read_only=True)

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'url',
            'preacher_name',
            'category_name',
            'preacher_ministry',
            'date_published',
            'description',
            'views'
        ]
