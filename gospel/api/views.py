import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Day
from .serializers import DaySerializer


class TodayGospel(APIView):

    def get(self, request, format=None):
        today = timezone.datetime.now()
        try:
            day = Day.objects.get(date=today)
            serializer = DaySerializer(day)
            return Response(serializer.data)
        except Day.DoesNotExist:
            return Response('Not Found', status=status.HTTP_404_NOT_FOUND)


class WeekPlan(APIView):

    def get(self, request, format=None):

        today = timezone.datetime.now()
        seven_days_later = timezone.datetime.now() + datetime.timedelta(days=6)

        days = Day.objects.filter(date__range=[today, seven_days_later])
        serializer = DaySerializer(days, many=True)

        return Response(serializer.data)
