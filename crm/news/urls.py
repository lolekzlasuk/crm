from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name="news_list"),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name="newsdetail"),
    path('unpublished/', views.UnpublishedNewsListView.as_view(), name="unpublished"),
    path('knowledge/',views.KnowledgeCategoryListView.as_view(), name="knowledge"),
    path('knowledge/<int:pk>', views.KnowledgeCategoryDetailView.as_view(), name="knowledgedetail"),
    path('upload/news', views.post_news, name="post_news"),
    path('upload/doc', views.post_document, name="createdoc"),
    path('upload/file', views.post_file, name="createfile"),
    path('upload/qanda', views.post_question, name="createquestion"),
    path('upload/userqanda', views.post_userquestion, name="createuserquestion"),
    path('news/<int:pk>/publish/', views.publish_news, name="publish_news"),
    path('flagtoggle/', views.flagtoggle, name="flagtoggle"),
    path('newstoggle/', views.newsreadflagtoggle, name="newsreadflag"),
    path('markall/', views.markall, name="markall"),
    path('docs/<int:pk>/', views.DocDetailView.as_view(), name="docdetail"),
    path('QandA/', views.QuestionListView.as_view(), name="QandA"),
    path('QandA/unanswered', views.UnansweredQuestionListView.as_view(), name="unanQandA"),
    path('upload/<int:pk>/updatequestion', views.answer_question, name="answerqna"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
