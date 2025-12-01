from datetime import date
from .serializers import YearSerializer
from .models import Year
from rest_framework import generics
from .serializers import MonthSerializer
from .models import Month
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DailyFamilyDevotional
from .serializers import DailyFamilyDevotionalSerializer
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# ✅ Fetch today's devotional
class TodayDevotionalView(APIView):
    def get(self, request):
        devotional = DailyFamilyDevotional.get_today_devotional()
        if devotional:
            serializer = DailyFamilyDevotionalSerializer(devotional)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No devotional found for today."}, status=status.HTTP_404_NOT_FOUND)


class DevotionalByDateView(APIView):
    def get(self, request, date):
        devotional = DailyFamilyDevotional.get_devotional_by_date(date)
        if devotional:
            serializer = DailyFamilyDevotionalSerializer(devotional)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No devotional found for the given date."}, status=status.HTTP_404_NOT_FOUND)


class NextDevotionalView(APIView):
    def get(self, request, date):
        current_devotional = DailyFamilyDevotional.get_devotional_by_date(date)
        if not current_devotional:
            return Response({"detail": "Devotional for the given date not found."}, status=status.HTTP_404_NOT_FOUND)

        next_devotional = current_devotional.get_next_devotional()
        if next_devotional:
            serializer = DailyFamilyDevotionalSerializer(next_devotional)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No next devotional available."}, status=status.HTTP_404_NOT_FOUND)


class PreviousDevotionalView(APIView):
    def get(self, request, date):
        current_devotional = DailyFamilyDevotional.get_devotional_by_date(date)
        if not current_devotional:
            return Response({"detail": "Devotional for the given date not found."}, status=status.HTTP_404_NOT_FOUND)

        previous_devotional = current_devotional.get_previous_devotional()
        if previous_devotional:
            serializer = DailyFamilyDevotionalSerializer(previous_devotional)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No previous devotional available."}, status=status.HTTP_404_NOT_FOUND)


class MonthlyDevotionalView(ListAPIView):
    queryset = Month.objects.all().order_by("id")
    serializer_class = MonthSerializer



# @method_decorator(cache_page(60 * 60), name='dispatch') 
class CurrentYearDevotionalView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            current_year = date.today().year
            year_instance, created = Year.objects.get_or_create(
                year=current_year)

            # Prefetch months, readings, and videos
            year_instance = (
                Year.objects
                .prefetch_related(
                    'months__daily_readings',
                    'months__videos'
                )
                .get(id=year_instance.id)
            )

            serializer = YearSerializer(year_instance)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
