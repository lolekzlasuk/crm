
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone
import datetime
from ..models import Day, Devent
from rest_framework_jwt.settings import api_settings
expire_delta             = api_settings.JWT_REFRESH_EXPIRATION_DELTA


jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class CalendarSerializer(serializers.ModelSerializer):

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



        # def create(self, validated_data):
        #
        #
        #     # print(validated_data)
        #     devent_obj = Devent(
        #             day = validated_data.get('day'),
        #             title = validated_data.get('title'),
        #             description = validated_data.get('description'),
        #             start = validated_data.get('start'),
        #             end = validated_data.get('end'))
        #
        #
        #     devent_obj.save()
        #     return devent_obj
