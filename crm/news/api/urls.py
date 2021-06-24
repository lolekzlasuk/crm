from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from .views import *
urlpatterns = [
    path('', NewsListDetailAPIView.as_view()),
    path('unpublished/', UnpublishedNewsListAPIView.as_view()),
    path('knowledge/', KnowledgeListAPIView.as_view()),
    path('faq/', DocQuestionListAPIView.as_view()),    
]
