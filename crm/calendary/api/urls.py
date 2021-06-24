from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', CalendarAPIView.as_view()),
    path('devent/', DeventDetailAPIView.as_view()),

]
