from django.contrib.auth import authenticate, get_user_model

from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from ..models import *
from .serializers import *
from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
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




class PostListAPIView(generics.ListAPIView, mixins.CreateModelMixin):
    permission_classes      = [permissions.IsAuthenticated]
    serializer_class        = PostListSerializer
    passed_id               = None

    def get_queryset(self):
        request         = self.request
        passed_id       = request.GET.get('id', None) or self.passed_id
        queryset        = Post.objects.all()

        if passed_id is not None:
            queryset = queryset.filter(category__id= passed_id)

        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetailAPIView(generics.RetrieveAPIView):
    permission_classes      = [permissions.IsAuthenticated]
    serializer_class        = PostSerializer
    queryset = Post.objects.all()


class CommentAPIView(generics.CreateAPIView):
    permission_classes      = [permissions.IsAuthenticated]
    serializer_class        = CommentCreationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)


class BoardCategoryListAPIView(generics.ListAPIView):
    permission_classes      = [permissions.IsAuthenticated]
    serializer_class        = BoardCategorySerializer
    queryset = BoardCategory.objects.all()
