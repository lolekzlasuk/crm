from django.urls import path
from . import views
app_name = 'suggestions'
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('employees/',views.EmployeeListView.as_view(),name="employees"),
    path('',views.QuestionListView.as_view(),name="questionlist"),
    path('upload/',views.post_question,name="questionform"),
    path('<int:pk>/answer',views.post_answer,name="postanswer"),
    
    path('category/<int:pk>',
        views.CategoryDetailView.as_view(),
        name="category"),

    path('<int:pk>',views.QuestionDetailView.as_view(),name="questiondetail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
