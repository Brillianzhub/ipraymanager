from .serializers import VideoSerializer
from .models import Video
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Video, Category
from .serializers import VideoSerializer, CategorySerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination


class VideoPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


# class VideoListCreateView(ListCreateAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer

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
