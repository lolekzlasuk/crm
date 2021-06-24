from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from .serializers import CalendarSerializer
from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from ..models import Day, Devent
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
import datetime
User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class DeventDetailAPIView(mixins.CreateModelMixin,
                          generics.RetrieveAPIView,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoObjectPermissions]
    serializer_class = CalendarSerializer
    passed_id = None
    queryset = Devent.objects.all()

    def get_object(self):
        request = self.request
        passed_id = request.GET.get('id', None) or self.passed_id
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        day = Day.objects.get(date__iexact=request.data['day']).pk
        request.data['day'] = day
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def patch(self, request, *args, **kwargs):
        day = Day.objects.get(date__iexact=request.data['day']).pk
        request.data['day'] = day
        return self.update(request, *args, **kwargs)


class CalendarAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CalendarSerializer

    def get_queryset(self):
        queryset = Devent.objects.all()
        min_date = self.request.query_params.get('min_date', None)
        max_date = self.request.query_params.get('max_date', None)
        if min_date is not None and max_date is not None:
            queryset = queryset.filter(
                day__date__lte=max_date, day__date__gte=min_date)
        elif max_date is None and min_date is not None:
            queryset = queryset.filter(day__date=min_date)
        else:
            queryset = queryset.filter(day__date__year=datetime.date.today().year,
                                       day__date__month=datetime.date.today().month)
        return queryset
