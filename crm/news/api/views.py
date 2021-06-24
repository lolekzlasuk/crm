from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from ..models import *
from .serializers import *
from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
import json
import copy
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
        self.perms_map = copy.deepcopy(self.perms_map)  # from EunChong's answer
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class UnpublishedNewsListAPIView(generics.ListAPIView):

    model = News
    permission_classes      = [permissions.IsAuthenticated]
    serializer_class        = NewsSerializer
    passed_id               = None

    def get_queryset(self):
        qs = News.objects.filter(published_date=None)
        return qs

class KnowledgeListAPIView(generics.ListAPIView):
    permission_classes      = [permissions.IsAuthenticated]
    serializer_class        = KnowledgeCategorySerializer
    queryset = KnowledgeCategory.objects.all()

class DocQuestionListAPIView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes      = [permissions.IsAuthenticated,permissions.DjangoModelPermissions, CustomDjangoModelPermission]
    serializer_class        = DocQuestionSerializer

    def get_queryset(self):

        queryset = DocQuestion.objects.exclude(answer=None)
        return queryset
    #different permissions for different views


#######views for uploading news docs docfiles

class UserQuestionListAPIView(generics.ListAPIView, generics.CreateAPIView,  CustomDjangoModelPermission):
    permission_classes      = [permissions.IsAuthenticated]
    serializer_class        = UserQuestionSerializer
    queryset = UserQuestion.objects.all()
    #different permissions for different views

class NewsListDetailAPIView(generics.ListAPIView, generics.RetrieveAPIView):
    model = News
    permission_classes      = [permissions.IsAuthenticated]
    serializer_class        = NewsSerializer
    passed_id               = None

    def get_queryset(self):
        userprofile = self.request.user.userprofile
        qs = News.objects.exclude(published_date=None).order_by('-published_date')
        qs = qs.filter(Q(target_location=userprofile.location) | Q(
            target_location="non"))
        qs = qs.filter(Q(target_departament=userprofile.departament) | Q(
            target_departament="non"))
        return qs

    def get_object(self):
        request         = self.request
        passed_id       = request.GET.get('id', None) or self.passed_id
        queryset        = self.get_queryset()
        obj             = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id = passed_id)
            self.check_object_permissions(request,obj)
        return obj

    def get(self, request, *args, **kwargs):
        url_passed_id       = request.GET.get('id', None)
        json_data           = {}
        body_               = request.body
        if is_json(body_):
            json_data           = json.loads(request.body)
            new_passed_id        = json_data.get('id',None)

        passed_id = url_passed_id or new_passed_id or None
        self.passed_id      = passed_id
        if passed_id is not None:
            return self.retrieve(request,*args,**kwargs)
        return super().get(request, *args, **kwargs)
