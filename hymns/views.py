# hymns/views.py

from rest_framework import generics
from .models import Hymn
from .serializers import HymnSerializer

# class HymnListAPIView(generics.ListAPIView):
#     queryset = Hymn.objects.all().order_by('title')
#     serializer_class = HymnSerializer

from django.utils.dateparse import parse_datetime
from rest_framework.exceptions import ValidationError

from django.utils.dateparse import parse_datetime


class HymnListAPIView(generics.ListAPIView):
    serializer_class = HymnSerializer

    def get_queryset(self):
        queryset = Hymn.objects.all().order_by('title')
        last_sync = self.request.query_params.get('last_sync')

        if last_sync:
            parsed_date = parse_datetime(last_sync)
            if parsed_date:
                queryset = queryset.filter(last_updated__gt=parsed_date)

        return queryset


class HymnDetailAPIView(generics.RetrieveAPIView):
    queryset = Hymn.objects.all()
    serializer_class = HymnSerializer
    lookup_field = 'id'
