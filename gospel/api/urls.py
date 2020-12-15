from django.urls import path
from rest_framework.routers import DefaultRouter

from .viewsets import DayViewSet
from .views import TodayGospel, WeekPlan

router = DefaultRouter()
router.register(r'calendar', DayViewSet, basename='calendar')

urlpatterns = [
    path('today/', TodayGospel.as_view()),
    path('weekplan/', WeekPlan.as_view()),
]

urlpatterns += router.urls