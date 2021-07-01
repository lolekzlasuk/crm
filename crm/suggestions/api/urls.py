from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from .views import *
urlpatterns = [
    path('', BoardCategoryListAPIView.as_view()),
    path('postlist/', PostListAPIView.as_view()),
    path('post/<int:pk>/', PostDetailAPIView.as_view()),
    path('comment/', CommentAPIView.as_view()),
]
