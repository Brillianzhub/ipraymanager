# views.py
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import PrayerWithScriptureContentSerializer
from rest_framework import generics
from rest_framework import status
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Prayer
from .serializers import PrayerSerializer
from django.views.decorators.cache import cache_page


from django.utils.dateparse import parse_datetime


@api_view(['GET'])
def get_all_prayers(request):
    last_sync = request.GET.get('last_sync')

    if last_sync:
        try:
            last_sync_dt = parse_datetime(last_sync)
            if last_sync_dt:
                prayers = Prayer.objects.filter(
                    last_updated__gt=last_sync_dt, publish=True)
            else:
                prayers = Prayer.objects.all()
        except Exception:
            prayers = Prayer.objects.all()
    else:
        prayers = Prayer.objects.all()

    prayers = prayers.only(
        'id', 'prayer_category', 'prayer',
        'prayer_scripture', 'featured', 'last_updated'
    ).order_by('id')

    serializer = PrayerSerializer(prayers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def prayers_meta(request):
    latest_update = Prayer.objects.order_by(
        '-last_updated').values_list('last_updated', flat=True).first()
    return Response({
        'last_updated': latest_update or now()
    })


@api_view(['POST'])
def create_prayer(request):
    serializer = PrayerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_prayers_by_scripture(request):
    scripture = request.query_params.get('scripture')
    if not scripture:
        return Response({"error": "scripture query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    prayers = Prayer.objects.filter(
        prayer_scripture__icontains=scripture, publish=True)
    serializer = PrayerSerializer(prayers, many=True)
    return Response(serializer.data)


class PrayerWithScriptureAPIView(generics.ListAPIView):
    queryset = Prayer.objects.filter(publish=True)
    serializer_class = PrayerWithScriptureContentSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def get_prayer_categories(request):
    categories = (
        Prayer.objects.values_list("prayer_category", flat=True)
        .distinct()
        .order_by("prayer_category")
    )
    return Response(categories, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_featured_prayers(request):
    prayers = Prayer.objects.filter(
        featured=True, publish=True).order_by("-last_updated")
    serializer = PrayerWithScriptureContentSerializer(prayers, many=True)
    return Response(serializer.data, status=200)
