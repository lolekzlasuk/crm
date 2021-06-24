from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from .serializers import UserRegisterSerializer, UserProfileSerializer, ChangePasswordSerializer
from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class UserProfileListAPIView(
        generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    passed_id = None

    def get_queryset(self):
        object_list = UserProfile.objects.all()
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')

            object_list = UserProfile.objects.all().filter(
                Q(name__icontains=query) | Q(email__icontains=query)
                | Q(departament__icontains=query) | Q(location__icontains=query)
                | Q(position__icontains=query) | Q(telephone__icontains=query)
            )

        return object_list


class UserProfileDetailAPIView(mixins.UpdateModelMixin,
                               generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_object(self):
        request = self.request
        object = get_object_or_404(
            UserProfile, pk=self.request.user.userprofile.pk)
        return object

    def put(self, request, *args, **kwargs):
        object = self.get_object()
        data = request.data
        if data.get('profile_pic') is not None:
            image = data.get('profile_pic')
            UserProfile.change_profile_pic(object, image)
            return Response("Profile Picture has been changed", status=status.HTTP_200_OK)
        else:
            object.set_default_profile_pic()
            return Response("Profile picture has been set to default", status=status.HTTP_200_OK)
        return super().get(request, *args, **kwargs)


class UserChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        object = self.request.user
        return object

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        self.object = self.get_object()

        if serializer.is_valid():
            data = serializer.data
            if not self.object.check_password(data.get("current_password")):
                return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            pw = data.get("new_password")
            pw2 = data.get("new_password2")
            if pw != pw2:
                return Response("passwords must match", status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(data.get("new_password"))
            self.object.save()
            return Response("Password has been changed", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RegisterAPIView(APIView):
#
#     permission_classes = [permissions.AllowAny]
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({'detail': "You are already authenticated"}, status=400)
#         data = request.data
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         password2 = data.get('password2')
#
#
#         qs = User.objects.filter(
#                 Q(username__iexact=username) |
#                 Q(email__iexact=username)
#                 )
#
#
#
#         if password != password2:
#             return Response({"detail":"password must match"}, status=401)
#         if qs.exists():
#             return Response({"detail":"this user already exists"}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             response = jwt_response_payload_handler(token, user, request=request)
#             return Response(response,status = 201)
#
#         return Response({"detail":"Invalid request"}, status=401)
#


class AuthAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': "You are already authenticated"}, status=400)
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        ).distinct()

        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(
                    token, user, request=request)
                return Response(response)
        return Response({"detail": "Invalid credentials"}, status=401)
