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
        elif len(content) > 256:
            content = {"error_code":433, "message":"正文内容不能超过256字", "data":None}
        elif len(pictures) > 9:
            content = {"error_code":433, "message":"图片最多只能上传9张", "data":None}
        elif len(content) == 0 and len(pictures) == 0:
            content = {"error_code":433, "message":"博客内容不能为空", "data":None}
        else:
            user = User.objects.get(username=username)
            blog=Blog.objects.create(user=user,content=content)
            for i,picture in enumerate(pictures):
                Picture.objects.create(blog=blog,image=picture,num=i)
            content = {"error_code": 200, "message": "博客发布成功", "data": None}
    #return render(request,'releaseBlog.html')
    return HttpResponse(json.dumps(content))

def get_blogs(request):
    # 获取用户发布过的所有博客
    # Arguments:
    #     request: It should contains {"username":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<dict>}
    #     Here data is a dictionary, its key is the release time(str) of the blog, and its value is a tuple (content,a list of  picture paths)
    content = {}
    data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":441,"message":"用户名不存在","data":None}
        else:
            user = User.objects.get(username=username)
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
                  }#测试的时候这里的时间都是一样的，所以只能获取到最后一条……
            content = {"error_code": 200, "message": "获取博客成功", "data": data}
    print(content)
    return HttpResponse(json.dumps(content))#这里dumps有问题

