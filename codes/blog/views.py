import re

from django.shortcuts import render,HttpResponse
from .models import Blog,Picture,Comment,Like,Tag,Topic
from user.models import User,Follow
from utils.utils import *
import datetime
import json
# Create your views here.

def generate_blog_content(b):
    contents = []
    users = []
    time = b.release_time.strftime("%Y-%m-%d %H:%M:%S")

    while b.repost_link != -1:
        contents.append(b.content)
        users.append(b.user.username)
        b = Blog.objects.get(id=b.repost_link)  

    pictures = Picture.objects.filter(blog=b)
    picture_paths = []
    for pic in pictures:
        picture_paths.append(str(pic.image))

    tags = Tag.objects.filter(blog=b)
    topics = []
    for tag in tags:
        topics.append(tag.topic.name)
    data = {
        'time': time,
        'origin_user': b.user.username,
        'origin_content': b.content,
        'users': users,
        'contents': contents,
        'pictures':picture_paths,
        'tags':topics,
    }

    return data

def release_blog(request):
    # 发布博客
    # Arguments:
    #     request: It should contains {"content":<str>,"pictures":<file>,"topics":<str>...} need Cookie
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
            topics = request.POST.getlist('topics')

            if len(text) > 256:
                content = {"error_code":433, "message":"正文内容不能超过256字", "data":None}
            elif len(pictures) > 9:
                content = {"error_code":433, "message":"图片最多只能上传9张", "data":None}
            elif len(text) == 0 and len(pictures) == 0:
                content = {"error_code":433, "message":"博客内容不能为空", "data":None}
            elif len(topics) > 10:
                content = {"error_code":433, "message":"话题最多只能添加10个", "data":None}
            else:
                blog=Blog.objects.create(user=user,content=text)
                for i,picture in enumerate(pictures):
                    Picture.objects.create(blog=blog,image=picture,num=i)
                for topic in topics:
                    if Topic.objects.filter(name=topic).exists() is False:
                        tpc=Topic.objects.create(name=topic)
                    else:
                        tpc = Topic.objects.get(name=topic)
                    Tag.objects.create(blog=blog,topic=tpc)
                content = {"error_code": 200, "message": "博客发布成功", "data": None}
    
    return HttpResponse(json.dumps(content))

def refresh_blogs(request):
    # 刷新动态主页，获得自己和关注对象的所有博客
    # Arguments:
    #     request: empty need Cookie
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<list>}
    content={}
    if request.method == 'POST':
        user = get_login_user(request)
        if user is None:
            content = {"error_code": 431, "message": "用户名不存在或当前未登录", "data": None}
        else:
            data = {}
            self_blogs = Blog.objects.filter(user=user)
            for b in self_blogs:
                data[b.id] = generate_blog_content(b)

            followships = Follow.objects.filter(from_user = user)
            for followship in followships:
                followee = followship.to_user
                follow_blogs = Blog.objects.filter(user=followee)
                for b in follow_blogs:
                    data[b.id] = generate_blog_content(b)

            content = {"error_code": 200, "message": "获取博客成功", "data": data}
    return HttpResponse(json.dumps(content))

def get_blogs(request):
    # 获取用户发布过的所有博客
    # Arguments:
    #     request: It should contains {"username":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<dict>}
    #     Here data is a dictionary, its key is the id of the blog, and its value is a dictionary (time<str>,original_user<str>,original_content<str>,users<list>,contents<int>,pictures<list>,tags<list>)

    content = {}
    data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":441,"message":"用户名不存在","data":None}
        else:
            user = User.objects.get(username=username)
            blogs = Blog.objects.filter(user = user)
            for b in blogs:
                data[b.id] = generate_blog_content(b)

            content = {"error_code": 200, "message": "获取博客成功", "data": data}
    return HttpResponse(json.dumps(content))

# 获取指定博客的点赞列表
def get_likes(request):
    # 获取指定博客的点赞列表
    # Arguments:
    #     request: It should contains {"blog_id":<int>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<list>>}
    content={}
    if request.method == 'POST':
        blog_id = int(request.POST.get('blog_id'))
        if Blog.objects.filter(id=blog_id).exists() is False:
            content = {"error_code": 442, "message": "目标博客不存在", "data": None}
        else:
            blog = Blog.objects.get(id=blog_id)
            like_usernames = []
            likes = Like.objects.filter(blog=blog)
            for lk in likes:
                like_usernames.append(lk.user.username)
            content = {"error_code": 200, "message": "点赞获取成功", "data": like_usernames}
    
    return HttpResponse(json.dumps(content))

# 获取指定博客的评论
def get_comments(request):
    # 获取指定博客的评论
    # Arguments:
    #     request: It should contains {"blog_id":<int>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<list>>}
    content={}
    if request.method == 'POST':
        blog_id = int(request.POST.get('blog_id'))
        if Blog.objects.filter(id=blog_id).exists() is False:
            content = {"error_code": 442, "message": "目标博客不存在", "data": None}
        else:
            blog = Blog.objects.get(id=blog_id)
            data = {}
            comments = Comment.objects.filter(blog=blog)
            for cmt in comments:
                data[cmt.id] = {
                    'time': cmt.release_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'username': cmt.user.username,
                    'blog_id':cmt.id,
                    'content':cmt.content,
                  }

            content = {"error_code": 200, "message": "评论获取成功", "data": data}
    
    return HttpResponse(json.dumps(content))

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
                blog_id = int(request.POST.get('blog_id'))
                if Blog.objects.filter(id=blog_id).exists() is False:
                    content = {"error_code": 442, "message": "转发的目标博客不存在", "data": None}
                else:
                    Blog.objects.create(user=user,content=text,repost_link=blog_id)

                    content = {"error_code": 200, "message": "博客转发成功", "data": None}
    
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
                target_blog = Blog.objects.get(id=target_blog_id)
                if Like.objects.filter(user=from_user,blog=target_blog).exists():
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
                target_blog = Blog.objects.get(id=target_blog_id)
                if Like.objects.filter(user=from_user, blog=target_blog).exists() is False:
                    content = {"error_code": 442, "message": "当前还未点赞", "data": None}
                else:
                    Like.objects.get(user=from_user, blog=target_blog).delete()
                    content = {"error_code": 200, "message": "取消点赞成功", "data": None}
    return HttpResponse(json.dumps(content))


def search_topic(request):
    # 查找话题
    # Arguments:
    #     request: It should contains {"keyword":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<list>}
    content = {}
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        topics_found = Topic.objects.filter(name__icontains = keyword)
        targets = [t.name for t in topics_found]
        content = {"error_code": 200, "message": "查找话题成功", "data": targets}
    return HttpResponse(json.dumps(content))

def hot_topics(request):
    # 查找热度（话题下总博客数）排名前十的话题
    # Arguments:
    #     request:
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<dict>}
    #     Here data is a dictionary, its key is the name of the topic, and its value is count<int>
    content = {}
    counts = {}
    if request.method == 'POST':
        topics = Topic.objects.all()
        for topic in topics:
            topic_name = topic.name
            counts[topic_name] = len(Tag.objects.filter(topic=topic_name))
        counts = sorted(counts.items(),key=lambda x:x[1],reverse=True)
        if len(counts)>10: length = 10
        else: length = len(counts)
        targets = [key for key,value in counts[:length]]
        content = {"error_code": 200, "message": "查找话题成功", "data": targets}
    return HttpResponse(json.dumps(content))


def get_topic_blogs(request):
    # 得到指定话题下的所有博客
    # Arguments:
    #     request: It should contains {"topic":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<dict>}
    #     Here data is a dictionary, its key is the id of the blog, and its value is a dictionary (time<str>,original_user<str>,original_content<str>,users<list>,contents<int>,pictures<list>,tags<list>)
    content = {}
    data = {}
    if request.method == 'POST':
        topic = request.POST.get('topic')
        if Topic.objects.filter(name=topic).exists() == False:
            content = {"error_code": 441, "message": "目标话题不存在", "data": None}
        else:
            tags = Tag.objects.filter(topic=topic)
            for tag in tags:
                blog = tag.blog
                data[blog.id] = generate_blog_content(blog)
            content = {"error_code": 200, "message": "查找博客成功", "data": data}
    return HttpResponse(json.dumps(content))


