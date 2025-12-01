from .serializers import CurrentLiveStreamSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import LiveStream
from .serializers import LiveStreamSerializer, LiveStreamLightSerializer


# List all livestreams or create a new one
class LiveStreamListCreateView(generics.ListCreateAPIView):
    queryset = LiveStream.objects.all()
    serializer_class = LiveStreamSerializer


# Retrieve, update, or delete a single livestream
""" class LiveStreamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LiveStream.objects.all()
    serializer_class = LiveStreamSerializer """


class CurrentLiveStreamView(APIView):
    def get(self, request):
        live = LiveStream.objects.filter(is_live=True).first()
        if live:
            serializer = LiveStreamSerializer(live)
            return Response(serializer.data)
        return Response({"is_live": False})


class LiveStreamDetailView(APIView):
    def get(self, request, pk):
        try:
            video = LiveStream.objects.get(id=pk)
        except LiveStream.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the selected video
        video_data = LiveStreamSerializer(video).data

        # Fetch related videos (excluding itself)
        related_videos = (
            LiveStream.objects.exclude(id=pk)
            .order_by('-created_at')[:4]
        )
        related_serializer = LiveStreamSerializer(related_videos, many=True)

        response_data = {
            **video_data,
            "related_videos": related_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class LiveStreamView(APIView):
    def get(self, request):
        live = LiveStream.objects.filter(is_live=True).first()

        if live:
            live_data = LiveStreamSerializer(live).data

            related_videos = (
                LiveStream.objects.filter(
                    is_live=False).order_by('-created_at')[:4]
            )

            related_serializer = LiveStreamSerializer(
                related_videos, many=True)

            response_data = {
                **live_data,
                "related_videos": related_serializer.data,
            }

            return Response(response_data)

        return Response({"is_live": False, "related_videos": []})


class CurrentLiveStatusView(APIView):
    def get(self, request):
        live = LiveStream.objects.filter(is_live=True).first()
        if live:
            serializer = CurrentLiveStreamSerializer(live)
            return Response(serializer.data)
        return Response({"is_live": False})


# views.py
class LiveStreamLightView(APIView):
    def get(self, request):
        streams = LiveStream.objects.filter(is_live=False).order_by("-created_at")[:10]

        serializer = LiveStreamLightSerializer(streams, many=True)
        return Response(serializer.data)


class LiveStreamIncrementView(APIView):
    def post(self, request, pk):
        try:
            livestream = LiveStream.objects.get(id=pk)
        except LiveStream.DoesNotExist:
            return Response(
                {"error": "Video not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Atomic increment
        livestream.viewer_count = F('viewer_count') + 1
        livestream.save(update_fields=['viewer_count'])
        livestream.refresh_from_db()  

        return Response(
            {"viewer_count": livestream.viewer_count},
            status=status.HTTP_200_OK
        )