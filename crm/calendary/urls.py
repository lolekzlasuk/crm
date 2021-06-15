from django.urls import path
from . import views
app_name = 'calendary'
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('<int:year>/<int:month>/',
        views.DayListView.as_view(), name="calendary"),

    path('<int:pk>/addevent/',views.post_devent,name="post_devent"),
    path('event/<int:pk>',views.DeventDetailView.as_view(),name="devent")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
