from django.shortcuts import render,HttpResponse
from .models import Blog,Picture
from user.models import User
import datetime
import json
# Create your views here.


def release_blog(request):
    # 发布博客
    # Arguments:
    #     request: It should contains {"username":<str>, "content":<str>,"pictures":<list>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}

    content={}
    if request.method == 'POST':
        username = request.POST.get('username')
        content = request.POST.get('content')
        pictures = request.FILES.getlist('pictures')

        if  User.objects.filter(username=username).exists()==False:
            content = {"error_code":431,"message":"用户名不存在","data":None}
        else:
            user = User.objects.get(username=username)
            blog=Blog.objects.create(user=user,content=content)
            for i,picture in enumerate(pictures):
                Picture.objects.create(blog=blog,image=picture,num=i)
            content = {"error_code": 200, "message": "博客发布成功", "data": None}
    #return render(request,'releaseBlog.html')
    return HttpResponse(json.dumps(content))

