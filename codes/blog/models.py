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
    return res

#博客
class Blog(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='blogs')     #发布博客的用户
    release_time = models.DateTimeField(auto_now_add=True)             #发布时间
    content = models.TextField()        #文本内容

#图片
class Picture(models.Model):
    blog = models.ForeignKey('blog.Blog',on_delete=models.CASCADE,related_name='pictures')      #图片所属的博客
    num = models.IntegerField()             # 图片编号
    image = models.ImageField(upload_to=direc_path)     #图片路径



