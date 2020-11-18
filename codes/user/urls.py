from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('register',views.resgister),
    path('sendRegisterCode',views.send_veri_code_register),
    path("sendLoginCode",views.send_veri_code_login),
    path('login',views.login),
    path('logout',views.logout),
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
    path('getUsername', views.get_username),
    path('follow',views.follow),
    path('cancelFollow',views.cancel_follow),
    path('getFollowers',views.get_followers),
    path('getFollowees',views.get_followees),
    path('test',views.test_add),
    path('getEmail',views.get_email),
    path('modifyPwdLogin',views.modify_password_login)
]
