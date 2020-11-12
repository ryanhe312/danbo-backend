from django.db import models

# Create your models here.


def direc_path(instance,filename):
    # 设置头像的存储路径
    # Arguments:
    #     instance , filename<str>
    # Return:
    #     the path
    ext=filename.split('.').pop()
    res = 'profiles/'+str(instance.user.username)+'.'+ext
    return res

#用户
class User(models.Model):
    username = models.CharField(max_length=20,unique='True')   #用户名
    password = models.CharField(max_length=100)   #密码
    email =  models.CharField(max_length=40,unique='True')     #邮箱
    nickname = models.CharField(max_length=20,default='游客')     #昵称
    signature = models.CharField(max_length=30,default="这个人很懒，什么都没留下",null=True,blank=True)  #签名
    birthday = models.DateField(null=True,blank=True)     #生日
    gender = models.CharField(max_length=1,null=True,blank=True,default="保密")      #性别
    address = models.CharField(max_length=40,null=True,blank=True,default="地址未填写")   #地址
#验证码
class VerificationCode(models.Model):
    email =  models.CharField(max_length=40,unique='True')      #邮箱
    code = models.CharField(max_length=4)        #验证码
    timestamp = models.FloatField()              #时间戳，发出时间

#头像
class Profile(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='profile')      #头像所属的用户
    image = models.ImageField(upload_to=direc_path)     #头像路径

#关注
class Follow(models.Model):
    to_user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='to_user')            #关注者
    from_user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='from_user')        #关注对象

    class Meta:
        unique_together = ("from_user", "to_user")      #组合键值