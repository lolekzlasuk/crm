import json
import copy
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status, mixins, viewsets
from rest_framework_jwt.settings import api_settings
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication
from ..models import News, NewsFile, Notification, NotificationReadFlag, \
    KnowledgeCategory, DocumentF, DocFile, DocQuestion, UserQuestion
from .serializers import NewsFileSerializer, FilteredListSerializer,  \
    DocumentFSmallSerializer, DocumentFSerializer, DocFileSerializer, \
    KnowledgeCategorySerializer, DocQuestionSerializer, UserQuestionSerializer, \
    DocFileUploadSerializer, NewsListSerializer, NewsCRUDSerializer
from accounts.models import UserProfile


User = get_user_model()


def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid


class CustomDjangoModelPermission(permissions.DjangoModelPermissions):

    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class KnowledgeListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions,
                          CustomDjangoModelPermission]
    serializer_class = KnowledgeCategorySerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        passed_id = request.GET.get('id', None) or self.passed_id
        queryset = KnowledgeCategory.objects.all()

        if passed_id is not None:
            queryset = queryset.filter(id=passed_id)

        return queryset


class DocQuestionListAPIView(
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions,
                          CustomDjangoModelPermission]
    serializer_class = DocQuestionSerializer

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        queryset = DocQuestion.objects.all()
        if self.request.user.groups.filter(name='Managers').exists():
            pass
        else:
            queryset = queryset.exclude(answer=None)

        if query is not None:
            queryset = queryset.filter(Q(title__icontains=query) | Q(
                answer__icontains=query) | Q(body__icontains=query))

        return queryset

    def get_object(self):
        request = self.request
        passed_id = request.GET.get('pk', None)
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, pk=passed_id)
            self.check_object_permissions(request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Managers').exists():
            return self.create(request, *args, **kwargs)
        else:
            return Response({'detail': 'You do not have permission to perform \
                this action.'}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserQuestionCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions,
                          CustomDjangoModelPermission]
    serializer_class = UserQuestionSerializer
    queryset = DocQuestion.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DocFileCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]
    serializer_class = DocFileUploadSerializer
    queryset = DocFile.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NewsFileCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]
    serializer_class = NewsFileSerializer
    queryset = NewsFile.objects.all()


class DocumentFViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions,
                          CustomDjangoModelPermission]
    serializer_class = DocumentFSerializer
    queryset = DocumentF.objects.all()


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions,
                          CustomDjangoModelPermission]
    serializer_classes = {
        'list': NewsListSerializer,
    }
    default_serializer_class = NewsCRUDSerializer
    queryset = News.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        news = self.get_object()
        if news.published_date != None:
            notification = Notification.objects.get(news=news)
            notificationreadflag = NotificationReadFlag.objects.get(
                user=user, notification=notification)
            notificationreadflag.read = True
            notificationreadflag.save()
        serializer = self.get_serializer(news)
        return Response(serializer.data)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action,
                                           self.default_serializer_class)

    def get_queryset(self):
        userprofile = self.request.user.userprofile
        qs = News.objects.all()
        if self.request.user.groups.filter(name='Managers').exists():
            pass
        else:
            qs = qs.exclude(
                published_date=None).order_by('-published_date')
            qs = qs.filter(Q(target_location=userprofile.location) | Q(
                target_location='non'))
            qs = qs.filter(Q(target_departament=userprofile.departament) | Q(
                target_departament='non'))
        return qs

    @action(detail=True, methods=['get'])
    def publish(self, request, pk=None):
        obj = News.objects.get(pk=pk)
        obj.publish()
        return Response({'published_date': obj.published_date},
                        status=status.HTTP_200_OK)
