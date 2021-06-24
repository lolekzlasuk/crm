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
jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class DeventDetailAPIView(mixins.CreateModelMixin,
    generics.RetrieveAPIView,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):
    permission_classes      = [permissions.IsAuthenticated, permissions.DjangoObjectPermissions]
    serializer_class        = CalendarSerializer
    passed_id               = None
    queryset = Devent.objects.all()

    def get_object(self):
        request         = self.request
        passed_id       = request.GET.get('id', None) or self.passed_id
        queryset        = self.get_queryset()
        obj             = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id = passed_id)
            self.check_object_permissions(request,obj)
        return obj

    def post(self, request, *args, **kwargs):
        day = Day.objects.get(date__iexact = request.data['day']).pk
        request.data['day'] = day
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

    def patch(self, request, *args, **kwargs):
        day = Day.objects.get(date__iexact = request.data['day']).pk
        request.data['day'] = day
        return self.update(request, *args, **kwargs)




class CalendarAPIView(generics.ListAPIView):
    permission_classes      = [permissions.IsAuthenticated]
    serializer_class        = CalendarSerializer
    passed_id               = None

    def get_queryset(self):
        queryset = Devent.objects.all()
        min_date = self.request.query_params.get('min_date', None)
        max_date = self.request.query_params.get('max_date', None)
        if min_date is not None and max_date is not None:
            queryset = queryset.filter(day__date__lte=max_date, day__date__gte=min_date)
        elif max_date is None and min_date is not None:
            queryset = queryset.filter(day__date = min_date)
        else:
            queryset = queryset.filter(day__date__year=datetime.date.today().year,
                              day__date__month=datetime.date.today().month)
        return queryset


        # data = self.request.data
        # start_date = data.get('date_range_start')
        # end_date = data.get('date_range_end')
        # if start_date is not None and end_date is not None:
        #     obj_list = object_list.exclude(Q(day__date__lt = start_date) | Q(day__date__gt = end_date))
        # return obj_list



#
# class UserProfileListAPIView(
#         generics.ListAPIView):
#
#
#     permission_classes      = [permissions.IsAuthenticated]
#     serializer_class        = UserProfileSerializer
#     passed_id               = None
#     def get_queryset(self):
#         object_list = UserProfile.objects.all()
#         if self.request.GET.get('q') != None:
#             query = self.request.GET.get('q')
#
#             object_list = UserProfile.objects.all().filter(
#                 Q(name__icontains=query) | Q(email__icontains=query)
#                 | Q(departament__icontains=query) | Q(location__icontains=query)
#                 | Q(position__icontains=query) | Q(telephone__icontains=query)
#             )
#
#         return object_list
#
#
#
# class UserProfileDetailAPIView(mixins.UpdateModelMixin,
#     generics.RetrieveAPIView):
#     permission_classes      = [permissions.IsAuthenticated]
#     serializer_class        = UserProfileSerializer
#     queryset                = UserProfile.objects.all()
#
#
#     def get_object(self):
#         request         = self.request
#         object = get_object_or_404(UserProfile, pk = self.request.user.userprofile.pk)
#         return object
#
#     def put(self, request, *args, **kwargs):
#         object = self.get_object()
#         data = request.data
#         if data.get('profile_pic') is not None:
#             image = data.get('profile_pic')
#             UserProfile.change_profile_pic(object,image)
#             return Response("Profile Picture has been changed",status=status.HTTP_200_OK)
#         else:
#             object.set_default_profile_pic()
#             return Response("Profile picture has been set to default",status=status.HTTP_200_OK)
#         return super().get(request, *args, **kwargs)
#
#
# class UserChangePasswordAPIView(APIView):
#     permission_classes      = [permissions.IsAuthenticated]
#     serializer_class        = ChangePasswordSerializer
#
#
#     def get_object(self, queryset=None):
#         object = self.request.user
#         return object
#
#     def put(self, request, *args, **kwargs):
#         serializer = ChangePasswordSerializer(data=request.data)
#         self.object = self.get_object()
#
#         if serializer.is_valid():
#             data = serializer.data
#             if not self.object.check_password(data.get("current_password")):
#                 return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             pw = data.get("new_password")
#             pw2 = data.get("new_password2")
#             if pw != pw2:
#                 return Response("passwords must match", status=status.HTTP_400_BAD_REQUEST)
#             self.object.set_password(data.get("new_password"))
#             self.object.save()
#             return Response("Password has been changed",status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#
# class AuthAPIView(APIView):
#
#     permission_classes = [permissions.AllowAny]
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({'detail': "You are already authenticated"}, status=400)
#         data = request.data
#         username = data.get('username')
#         password = data.get('password')
#
#         user = authenticate(username = username, password = password)
#         qs = User.objects.filter(
#                 Q(username__iexact=username) |
#                 Q(email__iexact=username)
#                 ).distinct()
#
#         if qs.count() == 1:
#             user_obj = qs.first()
#             if user_obj.check_password(password):
#                 user = user_obj
#                 payload = jwt_payload_handler(user)
#                 token = jwt_encode_handler(payload)
#                 response = jwt_response_payload_handler(token, user, request=request)
#                 return Response(response)
#         return Response({"detail":"Invalid credentials"}, status=401)
