from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.Post, name='post'),
    path('feed/', views.Feed, name='home'),
]
