from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
app_name = 'suggestions'

urlpatterns = [
    # path('employees/',views.EmployeeListView.as_view(),name="employees"),
    path('', views.PostListView.as_view(), name='postlist'),
    path('upload/', views.post_post, name='postform'),
    path('<int:pk>/comment', views.post_comment, name='postcomment'),

    path('category/<int:pk>', views.CategoryDetailView.as_view(), name="category"),

    path('<int:pk>', views.PostDetailView.as_view(), name='postdetail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
