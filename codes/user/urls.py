from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('register',views.resgister),
    path('sendRegisterCode',views.send_veri_code_regsiter),
    path("sendLoginCode",views.send_veri_code_login),
    path('login',views.login),
    path('verify',views.verify),
    path('modifyPwd',views.modify_password),
    path('modifyAddress',views.modify_address),
    path('modifyBirthday',views.modify_birthday),
    path('modifyGender',views.modify_gender),
    path('modifyNickname', views.modify_nickname),
    path('modifyProfile', views.modify_profile),
    path('modifySignature', views.modify_signature),
    path('getAddress', views.get_address),
    path('getBirthday', views.get_birthday),
    path('getGender', views.get_gender),
    path('getNickname', views.get_nickname),
    path('getProfile', views.get_profile_path),
    path('getSignature', views.get_signature),
    path('getblog', views.get_blogs),
]
