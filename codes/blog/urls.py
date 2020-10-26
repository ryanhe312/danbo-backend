from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('releaseBlog',views.release_blog),
    path('getBlog', views.get_blogs),
]
