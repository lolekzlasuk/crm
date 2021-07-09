from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from . import views
app_name = 'news-api'
router = DefaultRouter()
router.register('news', views.NewsViewSet)


urlpatterns = [
    path('router/', include(router.urls)),
    # path('', NewsListDetailAPIView.as_view()),
    # path('unpublished/', UnpublishedNewsListAPIView.as_view()),
    path('knowledge/', views.KnowledgeListAPIView.as_view()),
    path('faq/', views.DocQuestionListAPIView.as_view()),
    path('userquestion/', views.UserQuestionCreateAPIView.as_view()),
    path('uploaddocfile/', views.DocFileCreateAPIView.as_view()),
    path('createnewsfile/', views.NewsFileCreateAPIView.as_view())
]
