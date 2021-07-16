from rest_framework import generics, permissions
from .serializers import CalendarSerializer, CalendarListSerializer
from rest_framework import generics, mixins, permissions
from ..models import Day, Devent
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import datetime


class DeventDetailAPIView(
        generics.RetrieveAPIView,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):

    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoObjectPermissions]

    serializer_class = CalendarSerializer
    queryset = Devent.objects.all()



    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        day = Day.objects.get(date__iexact=request.data['day']).pk
        request.data['day'] = day
        return self.update(request, *args, **kwargs)


class CalendarAPIView(generics.ListAPIView, mixins.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CalendarListSerializer

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

    def post(self, request, *args, **kwargs):
        self.serializer_class = CalendarSerializer
        day = Day.objects.get(date__iexact=request.data['day']).pk
        request.data['day'] = day
        return self.create(request, *args, **kwargs)
