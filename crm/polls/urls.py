from django.urls import path
from . import views
app_name = 'polls'
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('employees/',views.EmployeeListView.as_view(),name="employees"),
    path('',views.PollListView.as_view(),name="polllist"),
    path('unpublished/',views.UnpublishedPollListView.as_view(),name="unpublishedpolllist"),
    path('<int:pk>/',views.createpollAnswer,name="createpollAnswer"),
    path('add/',views.post_Poll,name="pollform"),
    path('add/<int:pk>/',views.createpoll,name="createpoll"),
    path('publish/<int:pk>/',views.publishpoll,name="publishpoll"),
    path('answers/',views.PollListAnswerView.as_view(),name="answers"),
    path('answers/<int:pk>',views.PollAnswerDetailView.as_view(),name="detailanswers")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
