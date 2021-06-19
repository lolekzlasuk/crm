from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from .views import AuthAPIView, RegisterAPIView, UserProfileListAPIView
urlpatterns = [
    path('', AuthAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('jwt/', obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),
    path('list/', UserProfileListAPIView.as_view()),
]
