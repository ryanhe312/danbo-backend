from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('releaseBlog',views.release_blog),
    path('getBlog', views.get_blogs),
    path('repostBlog',views.repost_blog),
    path('giveLike',views.give_like),
    path('cancelLike',views.cancel_like),
    path('comment',views.comment),
    path('getComments',views.get_comments),
    path('getLikes',views.get_likes),
    path('refreshBlogs',views.refresh_blogs),
]
