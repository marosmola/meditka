from rest_framework import viewsets
from ..models import Day
from .serializers import DaySerializer


class DayViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
