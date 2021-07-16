from django.contrib import admin
from django.urls import path, include
from .views import DeventDetailAPIView, CalendarAPIView
urlpatterns = [
    path('', CalendarAPIView.as_view()),
    path('devent/<int:pk>/', DeventDetailAPIView.as_view()),
]
