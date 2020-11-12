from django.db import models

# Create your models here.

def direc_path(instance,filename):
    # 设置图片的存储路径
    # Arguments:
    #     instance , filename<str>
    # Return:
    #     the path
    ext=filename.split('.').pop()
    res = 'blog_images/'+'bid'+str(instance.blog.id)+"_pid"+str(instance.num)+'.'+ext
    # 测试注：是否有必要分用户文件夹、博客文件夹存储？
    return res

#博客
class Blog(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='blogs')     #发布博客的用户
    release_time = models.DateTimeField(auto_now_add=True)             #发布时间
    content = models.TextField(max_length=260)        #文本内容
    type = models.CharField(max_length=6,default='origin')      # 博客类型，只有两个有效值： 'origin'表示原创，'repost'表示转发
    repost_link = models.IntegerField(null=True)        #转发博客的Id, 若为原创博客，则该属性为null
#图片
class Picture(models.Model):
    blog = models.ForeignKey('blog.Blog',on_delete=models.CASCADE,related_name='pictures')      #图片所属的博客
    num = models.IntegerField()             # 图片编号
    image = models.ImageField(upload_to=direc_path)     #图片路径


#评论
class Comment(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='comment_user')     #发布评论的用户
    release_time = models.DateTimeField(auto_now_add=True)  # 发布时间
    blog = models.ForeignKey('blog.Blog',on_delete=models.CASCADE,related_name='comment_blog')      #评论的目标博客
    content = models.TextField(max_length=30)        #文本内容

#点赞
class Like(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='like_user')     #点赞的用户
    blog = models.ForeignKey('blog.Blog',on_delete=models.CASCADE,related_name='like_blog')     #点赞的博客对象

    class Meta:
        unique_together = ("user", "blog")          #组合键值
