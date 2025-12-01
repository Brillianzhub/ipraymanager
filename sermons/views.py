from rest_framework.views import APIView
from .models import Video
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Video, Category, Preacher
from .serializers import VideoSerializer, CategorySerializer, TopVideoSerializers, RecommendedVideoSerializer, FeaturedVideoSerializer, PreacherSerializer, PreacherCategorySerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination


class VideoPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


# 1. List all preachers
class PreacherListView(generics.ListAPIView):
    queryset = Preacher.objects.all()
    serializer_class = PreacherSerializer


# 2. List categories for a specific preacher
class PreacherCategoryListView(generics.ListAPIView):
    serializer_class = PreacherCategorySerializer

    def get_queryset(self):
        preacher_id = self.kwargs['preacher_id']
        return Category.objects.filter(videos__preacher_id=preacher_id).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['preacher_id'] = self.kwargs['preacher_id']
        return context


# 3. List videos for a specific preacher + category
class PreacherCategoryVideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        preacher_id = self.kwargs['preacher_id']
        category_id = self.kwargs['category_id']
        return Video.objects.filter(preacher_id=preacher_id, category_id=category_id)


# 4. Video detail view
class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = "id"


@api_view(['GET'])
def get_sermons(request):
    category_name = request.GET.get('category')
    videos = Video.objects.all().order_by('-date_added')

    if category_name:
        videos = videos.filter(category__name__iexact=category_name)

    paginator = VideoPagination()
    result_page = paginator.paginate_queryset(videos, request)
    serializer = VideoSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def increment_video_views(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
        video.views += 1
        video.save(update_fields=["views"])
        return Response({"views": video.views}, status=status.HTTP_200_OK)
    except Video.DoesNotExist:
        return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def total_counts(request):
    # hymn_count = Hymn.objects.count()
    sermon_count = Video.objects.count()
    # prayer_point_count = PrayerPoint.objects.count()

    return Response({
        # 'hymns': hymn_count,
        'sermons': sermon_count,
        # 'prayer_points': prayer_point_count,
    })


class IncrementVideoViews(APIView):
    def post(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
            video.views = video.views + 1
            video.save(update_fields=['views'])
            return Response({"views": video.views}, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def featured_sermons(request):
    """
    Return the 4 latest published featured videos for the homepage.
    """
    videos = (
        Video.objects.filter(featured=True, date_published__isnull=False)
        .order_by('-date_published')[:4]
    )
    serializer = FeaturedVideoSerializer(videos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recommended_sermons(request):
    """
    Return the 4 latest published featured videos for the homepage.
    """
    videos = (
        Video.objects.filter(recommended=True, date_published__isnull=False)
        .order_by('-date_published')[:6]
    )
    serializer = RecommendedVideoSerializer(videos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def most_viewed_sermons(request):
    top_videos = Video.objects.most_viewed(limit=4)
    serializer = TopVideoSerializers(top_videos, many=True)
    return Response(serializer.data)
