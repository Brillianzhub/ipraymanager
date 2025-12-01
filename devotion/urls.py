# urls.py
from django.urls import path
from .views import TodayDevotionalView, DevotionalByDateView, CurrentYearDevotionalView, NextDevotionalView, PreviousDevotionalView, MonthlyDevotionalView

urlpatterns = [
    path('today/', TodayDevotionalView.as_view(),
         name='today_devotional'),
    path('devotional/<str:date>/previous/',
         PreviousDevotionalView.as_view(), name='previous_devotional'),
    path('devotional/<str:date>/next/',
         NextDevotionalView.as_view(), name='next_devotional'),
    path('timetable/',
         CurrentYearDevotionalView.as_view(), name='timetable'),
    path('<str:date>/', DevotionalByDateView.as_view(),
         name='devotional_by_date'),
]
