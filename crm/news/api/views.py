from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from ..models import *
from .serializers import *
from rest_framework import generics, mixins, permissions, viewsets
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
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


# class UnpublishedNewsListAPIView(generics.ListAPIView):
#
#     model = News
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = NewsListSerializer
#
#     def get_queryset(self):
#         qs = News.objects.filter(published_date=None)
#         return qs



class KnowledgeListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = KnowledgeCategorySerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        passed_id = request.GET.get('id', None) or self.passed_id
        queryset = KnowledgeCategory.objects.all()

        if passed_id is not None:
            queryset = queryset.filter(id=passed_id)

        return queryset

# add a search here and retrieve questioins
class DocQuestionListAPIView(generics.ListAPIView, mixins.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions,
                          CustomDjangoModelPermission]
    serializer_class = DocQuestionSerializer

    def get_queryset(self):
        queryset = DocQuestion.objects.exclude(answer=None)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



# views for uploading news docs docfiles



class UserQuestionListAPIView(generics.ListAPIView, mixins.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions,
                          CustomDjangoModelPermission]
    serializer_class = UserQuestionSerializer
    queryset = UserQuestion.objects.all()


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DocFileCreateAPIView(generics.CreateAPIView):
        permission_classes = [permissions.IsAuthenticated,
                              permissions.DjangoModelPermissions]
        serializer_class = DocFileUploadSerializer
        queryset = DocFile.objects.all()

class NewsViewSet(viewsets.ModelViewSet):
    # mapping serializer into the action
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions,
                          CustomDjangoModelPermission]
    serializer_classes = {
        'list': NewsListSerializer,
    }
    default_serializer_class = NewsCRUDSerializer # Your default serializer
    queryset = News.objects.all()
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        userprofile = self.request.user.userprofile
        qs = News.objects.exclude(
            published_date=None).order_by('-published_date')
        qs = qs.filter(Q(target_location=userprofile.location) | Q(
            target_location="non"))
        qs = qs.filter(Q(target_departament=userprofile.departament) | Q(
            target_departament="non"))
        return qs

# class NewsListDetailAPIView(generics.ListAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
#     model = News
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = NewsSerializer
#     passed_id = None
#
#     def get_queryset(self):
#         userprofile = self.request.user.userprofile
#         qs = News.objects.exclude(
#             published_date=None).order_by('-published_date')
#         qs = qs.filter(Q(target_location=userprofile.location) | Q(
#             target_location="non"))
#         qs = qs.filter(Q(target_departament=userprofile.departament) | Q(
#             target_departament="non"))
#         return qs
#
#     def get_object(self):
#         request = self.request
#         passed_id = request.GET.get('id', None) or self.passed_id
#         queryset = self.get_queryset()
#         obj = None
#         if passed_id is not None:
#             obj = get_object_or_404(queryset, id=passed_id)
#             self.check_object_permissions(request, obj)
#         return obj
#
#     def get(self, request, *args, **kwargs):
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         body_ = request.body
#         if is_json(body_):
#             json_data = json.loads(request.body)
#             new_passed_id = json_data.get('id', None)
#
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
#         if passed_id is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return super().get(request, *args, **kwargs)
#
#
#
# # class RequestViewSet(viewsets.ModelViewSet):
# #     serializer_class = RequestModelSerializer
# #     model = Request
# #
# #     def get_serializer_class(self):
# #         serializer_class = self.serializer_class
# #         if self.request.method == 'POST':
# #             serializer_class = SerializerWithoutCertainFields
# #         return serializer_class
