from rest_framework import serializers
from ..models import Day, Gospel


class GospelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gospel
        exclude = ['id', 'day']


class DaySerializer(serializers.ModelSerializer):
    gospels = GospelSerializer(many=True, read_only=True)

    class Meta:
        model = Day
        fields = ['date', 'dayofweek', 'nameday', 'saintsday', 'gospels']
