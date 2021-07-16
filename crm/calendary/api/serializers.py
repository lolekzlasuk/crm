from rest_framework import serializers
from django.utils import timezone
import datetime
from ..models import Day, Devent




class CalendarSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
    class Meta:
        model = Devent
        fields = [
        'id',
        'day' ,
        'title',
        'description',
        'start',
        'end',
        'author'
        ]
        read_only_fields = ['id','author']

    def to_representation(self, instance):
        rep = super(CalendarSerializer, self).to_representation(instance)
        rep['day'] = instance.day.date
        return rep

class CalendarListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Devent
        fields = [
        'id',
        'day' ,
        'title',
        'start',
        'end',
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        rep = super(CalendarListSerializer, self).to_representation(instance)
        rep['day'] = instance.day.date
        return rep
