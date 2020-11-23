from django.shortcuts import render,HttpResponse
from user.models import  User


def get_login_user(request):
    # 获取当前登录用户
    # Arguments:
    #     request
    # Return:
    #     None if cookie not exist or target user not exist
    #     user object if the target user exists
    username = request.COOKIES.get('username')
    if not username or not User.objects.filter(username=username).exists():
        return None
    else:
        return User.objects.get(username=username)
