from django.urls import path
from . import views
app_name = 'polls'
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('employees/',views.EmployeeListView.as_view(),name="employees"),
    path('',views.PollListView.as_view(),name="poll_list"),
    path('unpublished/',views.UnpublishedPollListView.as_view(),name="unpublishedpolllist"),
    path('<int:pk>/',views.create_poll_answer,name="create_poll_answer"),
    path('add/',views.post_Poll,name="pollform"),
    path('add/<int:pk>/',views.create_poll_question,name="create_poll_question"),
    path('publish/<int:pk>/',views.publishpoll,name="publishpoll"),
    path('submitions/',views.PollListAnswerView.as_view(),name="poll_submitions"),
    path('submitions/<int:pk>',views.PollAnswerDetailView.as_view(),name="detailanswers")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
