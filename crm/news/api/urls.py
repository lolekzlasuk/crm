from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import *
router = DefaultRouter()
router.register('news', NewsViewSet)


urlpatterns = [
    path('router/', include(router.urls)),
    # path('', NewsListDetailAPIView.as_view()),
    # path('unpublished/', UnpublishedNewsListAPIView.as_view()),
    path('knowledge/', KnowledgeListAPIView.as_view()),
    path('faq/', DocQuestionListAPIView.as_view()),
    path('userquestion/', UserQuestionListAPIView.as_view()),
    path('uploaddocfile/', DocFileCreateAPIView.as_view()),
]
