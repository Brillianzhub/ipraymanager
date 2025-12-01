from .serializers import ArtistSerializer, MusicSerializer, RelatedArtistSerializer, DetailMusicSerializer
from .models import Artist, Music
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class MusicPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 30


def list_artists(request):
    artists = Artist.objects.only("id", "name", "image", "country")
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)


def songs_by_artist(request, artist_id):
    songs = Music.objects.filter(artist_id=artist_id)
    serializer = MusicSerializer(songs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_music(request):
    query = request.GET.get("q", "")

    results = Music.objects.filter(title__icontains=query)

    if results.exists():
        serializer = MusicSerializer(results, many=True)
        return Response({"found": True, "results": serializer.data})

    suggestions = Music.objects.filter(
        Q(title__icontains=query[:3]) |
        Q(category__icontains=query) |
        Q(artist__name__icontains=query)
    )[:10]

    serializer = MusicSerializer(suggestions, many=True)
    return Response({"found": False, "suggestions": serializer.data})

def songs_by_category(request, category):
    songs = Music.objects.filter(category__iexact=category)
    serializer = MusicSerializer(songs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def paginated_music(request):
    songs = Music.objects.all().order_by('-date_added')
    paginator = MusicPagination()
    result = paginator.paginate_queryset(songs, request)
    serializer = MusicSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def top_trending(request):
    trending = Music.objects.all().order_by('-views')[:6]
    serializer = MusicSerializer(trending, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def increment_music_views(request, pk):
    try:
        song = Music.objects.get(pk=pk)
        song.views += 1
        song.save(update_fields=['views'])
        return Response({"message": "View added", "views": song.views}, status=200)
    except Music.DoesNotExist:
        return Response({"error": "Song not found"}, status=404)



@api_view(['GET'])
def get_music_with_related(request, pk):
    try:
        song = Music.objects.get(id=pk)
    except Music.DoesNotExist:
        return Response({"error": "Music not found"}, status=404)

    # First, attempt to get related songs by SAME ARTIST
    related_by_artist = Music.objects.filter(
        artist=song.artist
    ).exclude(id=song.id)[:5]  

    # If less than 4, fill with songs from SAME CATEGORY
    if related_by_artist.count() < 5:
        needed = 5 - related_by_artist.count()
        related_by_category = Music.objects.filter(
            category=song.category
        ).exclude(id__in=[song.id] + list(related_by_artist.values_list('id', flat=True)))[:needed]

        # Combine both
        related_songs = list(related_by_artist) + list(related_by_category)
    else:
        related_songs = list(related_by_artist)

    return Response({
        "song": DetailMusicSerializer(song).data,
        "related": MusicSerializer(related_songs, many=True).data
    })
