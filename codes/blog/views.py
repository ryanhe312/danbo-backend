from django.shortcuts import render,HttpResponse
from .models import Blog,Picture,Comment,Like
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
            text = request.POST.get('content')
            pictures = request.FILES.getlist('pictures')
            if len(text) > 256:
                content = {"error_code":433, "message":"正文内容不能超过256字", "data":None}
            elif len(pictures) > 9:
                content = {"error_code":433, "message":"图片最多只能上传9张", "data":None}
            elif len(text) == 0 and len(pictures) == 0:
                content = {"error_code":433, "message":"博客内容不能为空", "data":None}
            else:
                blog=Blog.objects.create(user=user,content=text)
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
    #     Here data is a dictionary, its key is the release time(str) of the blog, and its value is a dictionary (blog_id<int>,type<str>,content<str>,pictures<list>,repost_link<int>,comments<list>, likes<list>)
    #       pcitures:list of picture paths<str>
    #       comments: list of comment ids<int>
    #       likes: list of like usernames<str>
    #       type：only 2 valid values: 'origin' or 'repost'

    content = {}
    data = {}
    if request.methvod == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":441,"message":"用户名不存在","data":None}
        else:
            user = User.objects.get(username=username)
            blogs = Blog.objects.filter(user = user)
            for b in blogs:
                pictures = Picture.objects.filter(blog=b)
                picture_paths = []
                for pic in pictures:
                    picture_paths.append(str(pic.image))
                    # 测试注：暂时修改为只传文件路径，不加str无法应用json

                comment_ids = []
                comments = Comment.objects.filter(blog=b)
                for cmt in comments:
                    comment_ids.append(cmt.id)
                like_usernames = []
                likes = Like.objects.filter(blog=b)
                for lk in likes :
                    like_usernames.append(lk.user)
                data[b.release_time.strftime("%Y-%m-%m %H:%M:%S")] = {
                    'blog_id':b.id,
                    'type':b.type,
                    'content':b.content,
                    'pictures':picture_paths,
                    'repost_link':b.repost_link,
                    'comments':comment_ids,
                    'likes':like_usernames,
                  }
            content = {"error_code": 200, "message": "获取博客成功", "data": data}
    return HttpResponse(json.dumps(content))#这里dumps有问题

# 转发博客
def repost_blog(request):
    # 转发博客
    # Arguments:
    #     request: It should contains {"content":<str>,"blog_id":<int>} need Cookie
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content={}
    if request.method == 'POST':
        user = get_login_user(request)
        if user is None:
            content = {"error_code": 431, "message": "用户名不存在或当前未登录", "data": None}
        else:
            text = request.POST.get('content')

            if len(text) > 100:
                content = {"error_code":433, "message":"转发正文内容不能超过100字", "data":None}
            else:
                blog_id = request.get('blog_id')
                if Blog.objects.filter(id=blog_id).exists() is False:
                    content = {"error_code": 442, "message": "转发的目标博客不存在", "data": None}
                else:
                    Blog.objects.create(user=user,content=text,type='repost',repost_link=blog_id )

                    content = {"error_code": 200, "message": "博客转发成功", "data": None}
    #return render(request,'releaseBlog.html')
    return HttpResponse(json.dumps(content))

#评论
def comment(request):
    # 发布评论
    # Arguments:
    #     request: It should contains {"content":<str>,"blog_id":<int>} need Cookie
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content={}
    if request.method == 'POST':
        user = get_login_user(request)
        if user is None:
            content = {"error_code": 431, "message": "用户名不存在或当前未登录", "data": None}
        else:
            blog_id = request.POST.get('blog_id')
            text = request.POST.get('content')
            if Blog.objects.filter(id=blog_id).exists() is False:
                content = {"error_code": 443, "message": "评论的目标博客不存在", "data": None}
            elif len(text) > 30:
                content = {"error_code":433, "message":"评论内容不能超过30字", "data":None}
            elif len(text) == 0 :
                content = {"error_code":433, "message":"评论内容不能为空", "data":None}
            else:
                target_blog = Blog.objects.get(id=blog_id)
                Comment.objects.create(user=user,blog=target_blog,content=text)
                content = {"error_code": 200, "message": "评论成功", "data": None}

    return HttpResponse(json.dumps(content))

def give_like(request):
    # 点赞操作
    # Arguments:
    #     request: It should contains {"blog_id":<int>} need Cookie
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        from_user = get_login_user(request)
        if from_user is None:
            content = {"error_code": 431, "message": "用户名不存在或当前未登录", "data": None}
        else:
            target_blog_id = request.POST.get('blog_id')
            if Blog.objects.filter(id=target_blog_id).exists() == False:
                content = {"error_code": 441, "message": "点赞的目标博客不存在", "data": None}
            else:
                target_blog = User.objects.get(id=target_blog_id)
                if Like.objects.filter(user=from_user,blog=target_blog).exist():
                    content = {"error_code": 442, "message": "请不要重复点赞", "data": None}
                else:
                    Like.objects.create(user=from_user,blog=target_blog)
                    content = {"error_code": 200, "message": "点赞成功", "data": None}
    return HttpResponse(json.dumps(content))

def cancel_like(request):
    # 取消点赞操作
    # Arguments:
    #     request: It should contains {"blog_id":<int>} need Cookie
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        from_user = get_login_user(request)
        if from_user is None:
            content = {"error_code": 431, "message": "用户名不存在或当前未登录", "data": None}
        else:
            target_blog_id = request.POST.get('blog_id')
            if Blog.objects.filter(id=target_blog_id).exists() == False:
                content = {"error_code": 441, "message": "取消点赞的目标博客不存在", "data": None}
            else:
                target_blog = User.objects.get(id=target_blog_id)
                if Like.objects.filter(user=from_user, blog=target_blog).exist() is False:
                    content = {"error_code": 442, "message": "当前还未点赞", "data": None}
                else:
                    Like.objects.get(user=from_user, blog=target_blog).delete()
                    content = {"error_code": 200, "message": "取消点赞成功", "data": None}
    return HttpResponse(json.dumps(content))


def test(request):
    # 仅供后端测试使用

    # # 测试发布博客
    # username = 'Sun'
    # user = User.objects.get(username=username)
    # content = "How are you"
    # Blog.objects.create(user=user,content=content)

    # #测试评论
    # blog = Blog.objects.get(id=1)
    # user = User.objects.get(username='Sun')
    # content = 'Hi'
    # Comment.objects.create(user=user,content=content,blog=blog)

    # #测试转发
    # blog = Blog.objects.get(id=3)
    # user = User.objects.get(username='Wang')
    # content = 'I am fine'
    # Blog.objects.create(user=user,content=content,type='repost',repost_link=blog.id)

    # # 测试点赞
    # blog = Blog.objects.get(id=1)
    # user = User.objects.get(username='Sun')
    # Like.objects.create(user=user,blog=blog)

    # # 测试取消点赞
    # blog = Blog.objects.get(id=1)
    # user = User.objects.get(username='Sun')
    # Like.objects.get(user=user,blog=blog).delete()


    # # 测试查询给定用户所有的博客
    # data = {}
    # user = User.objects.get(username='Wang')
    # blogs = Blog.objects.filter(user=user)
    # for b in blogs:
    #     pictures = Picture.objects.filter(blog=b)
    #     picture_paths = []
    #     for pic in pictures:
    #         picture_paths.append(str(pic.image))
    #
    #     comment_ids = []
    #     comments = Comment.objects.filter(blog=b)
    #     for cmt in comments:
    #         comment_ids.append(cmt.id)
    #     like_usernames = []
    #     likes = Like.objects.filter(blog=b)
    #     for lk in likes:
    #         like_usernames.append(lk.user.username)
    #     data[b.release_time.strftime("%Y-%m-%m %H:%M:%S")] = {
    #         'blog_id': b.id,
    #         'type': b.type,
    #         'content': b.content,
    #         'pictures': picture_paths,
    #         'repost_link': b.repost_link,
    #         'comments': comment_ids,
    #         'likes': like_usernames,
    #     }
    #
    # print(data)
    return HttpResponse('HH')