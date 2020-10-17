from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('register',views.resgister),
    path('test',views.test),
    path('pictest',views.test),
    path('verify',views.send_veri_code_regsiter),
    path('login',views.login),
    path('getblog',views.get_blogs),
]
