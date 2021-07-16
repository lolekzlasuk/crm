from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KnowledgeListAPIView, DocQuestionListAPIView, \
    UserQuestionCreateAPIView, DocFileCreateAPIView, NewsFileCreateAPIView, \
    NewsViewSet, DocumentFViewSet

app_name = 'news-api'
router = DefaultRouter()
router.register('news', NewsViewSet, basename='news')
router.register('documents', DocumentFViewSet, basename='documents')

urlpatterns = [
    path('', include(router.urls)),
    path('knowledge/', KnowledgeListAPIView.as_view()),
    path('faq/', DocQuestionListAPIView.as_view()),
    path('userquestion/', UserQuestionCreateAPIView.as_view()),
    path('uploaddocfile/', DocFileCreateAPIView.as_view()),
    path('createnewsfile/', NewsFileCreateAPIView.as_view())
]
