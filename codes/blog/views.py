from django.shortcuts import render,HttpResponse
from .models import Blog,Picture
from user.models import User
import datetime
import json
# Create your views here.

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


def release_blog(request):
    # 发布博客
    # Arguments:
    #     request: It should contains {"content":<str>,"pictures":<file>,"pictures":<file>...} need Cookie
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}

    content={}
    if request.method == 'POST':
        user = get_login_user(request)
        if user is None:
            content = {"error_code": 431, "message": "用户名不存在或当前未登录", "data": None}
        else:
            content = request.POST.get('content')
            pictures = request.FILES.getlist('pictures')
            if len(content) > 256:
                content = {"error_code":433, "message":"正文内容不能超过256字", "data":None}
            elif len(pictures) > 9:
                content = {"error_code":433, "message":"图片最多只能上传9张", "data":None}
            elif len(content) == 0 and len(pictures) == 0:
                content = {"error_code":433, "message":"博客内容不能为空", "data":None}
            else:
                blog=Blog.objects.create(user=user,content=content)
                for i,picture in enumerate(pictures):
                    Picture.objects.create(blog=blog,image=picture,num=i)
                content = {"error_code": 200, "message": "博客发布成功", "data": None}
    #return render(request,'releaseBlog.html')
    return HttpResponse(json.dumps(content))

def get_blogs(request):
    # 获取用户发布过的所有博客
    # Arguments:
    #     request: need Cookie
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<dict>}
    #     Here data is a dictionary, its key is the release time(str) of the blog, and its value is a tuple (content,a list of  picture paths)
    content = {}
    data = {}
    if request.method == 'POST':
        user = get_login_user(request)
        if user is None:
            content = {"error_code": 431, "message": "用户名不存在或当前未登录", "data": None}
        else:
            blogs = Blog.objects.filter(user_id = user.id)
            for b in blogs:
                pictures = Picture.objects.filter(blog=b)
                picture_paths = []
                for pic in pictures:
                    picture_paths.append(str(pic.image))
                    # 测试注：暂时修改为只传文件路径，不加str无法应用json
                data[b.release_time.strftime("%Y-%m-%m %H:%M:%S")] = {
                    'content':b.content,
                    'pictures':picture_paths
                  }
            content = {"error_code": 200, "message": "获取博客成功", "data": data}
    return HttpResponse(json.dumps(content))#这里dumps有问题

