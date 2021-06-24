from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from .views import *
urlpatterns = [
    path('', CalendarAPIView.as_view()),
    path('devent/', DeventDetailAPIView.as_view()),

]
