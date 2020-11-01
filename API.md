# **蛋博Web API文档**

版本20201101.6

 

UPD：请求格式，加入Cookie

## **一、简介**

1. 请求使用HTTP协议的multipart/form-data格式，需要包含相应的键值对。格式描述如下：

name:type

name表示键值名，type表示键值类型，包括text文本和file文件两种。



2. 除登陆、注册、找回密码功能外，所有请求必须包含一个Cookie，这个Cookie在登陆时加入，在登出时删除。



3. 返回值按如下JSON格式发送：

{

​	"err_code": <int, 200 means success, otherwise fail>,

​	"message": <str, human-readable message replied from the server>,

​	"data": <data, this part is different from api to api>

}

 

4. 错误码规范为：

 

* 前两位标明功能40 注册 41登陆 42 修改密码 43修改属性 44获取属性

* 第三位标明错误1 不存在 2 不正确 3 格式错误

* 200表示成功执行。

 

5. 图像获取的是相对路径，绝对路径为：MEDIA_ROOT + 相对路径，MEDIA_ROOT = 127.0.0.1:8000/media/ 部署在不同服务器上时，请用真实IP地址和端口

 

## **二、用户API（user）**

用户API都以 /user/ 开头，包含用户的登陆，注册，找回密码，修改属性和获取属性等功能。

 

用户包括用户名，密码，邮箱，昵称，头像路径，签名，生日，性别，地址字段。

验证码包括邮箱，验证码，时间戳，发出时间字段。

头像包括头像属于的用户，图像字段。



### **1.注册**

请求地址：/user/register

请求方式：POST

请求内容：

 

username:text

password:text

r_password:text

email:text

code:text

 

返回内容：

{"error_code":401,"message":"用户名已注册","data":None}

{"error_code":401,"message":"邮箱已注册","data":None}

{"error_code": 402, "message": "密码只能由大小写字母，数字组成，且长度应在6-20", "data": None}

{"error_code":402,"message":"两次输入的密码不一致","data":None}

{"error_code": 403, "message": "邮箱格式不正确", "data": None}

{"error_code": 403, "message": "验证码不正确或已过期", "data": None}

{"error_code": 200, "message": "注册成功", "data": None}

 

 

### **2.发送注册验证码**

向用户邮箱发送注册验证码

 

请求地址：/user/sendRegisterCode

请求方式：POST

请求内容：

email:text

 

返回内容：

{"error_code":401,"message":"邮箱已注册","data":None}

{"error_code": 403, "message": "邮箱格式不正确", "data": None}

{"error_code": 200, "message": "邮件发送成功", "data": None}

 

### **3.找回密码**

请求地址：/user/modifyPwd

请求方式：POST

请求内容：

 

username:text

password:text

r_password:text

email:text

code:text

 

返回内容：

{"error_code":421,"message":"用户名不存在","data":None}

{"error_code": 423, "message": "密码只能由大小写字母，数字组成，且长度应在6-20", "data": None}

{"error_code":422,"message":"两次输入的密码不一致","data":None}

{"error_code": 423, "message": "邮箱格式不正确", "data": None}

{"error_code": 422, "message": "该邮箱不是您注册时填写的邮箱", "data": None}

{"error_code": 422, "message": "验证码不正确或已过期", "data": None}

{"error_code": 200, "message": "密码修改成功", "data": None}

 

### **4.发送找回密码验证码**

向用户邮箱发送登录时找回密码的验证码

 

请求地址：/user/sendLoginCode

请求方式：POST

请求内容：

email:text

 

返回内容：

{"error_code": 423, "message": "邮箱格式不正确", "data": None}

{"error_code": 422, "message": "该邮箱不是您注册时填写的邮箱", "data": None}

{"error_code": 200, "message": "邮件发送成功", "data": None}

 

### **5.登陆**

请求地址：/user/login

请求方式：POST

请求内容：

username:text

password:text

 

返回内容：

{"error_code": 411, "message": "用户不存在", "data": None}

{"error_code": 412, "message": "密码不正确", "data": None}

{"error_code": 200, "message": "登录成功", "data": None}

 

### 6.登出

请求地址：/user/logout

请求方式：POST

请求内容：需要Cookie

 

返回内容：

{"error_code": 411, "message": "当前未登录", "data": None}

{"err_code": 200, "message": "成功退出登录", "data": None}



### **6.修改地址**

请求地址：/user/modifyAddress

请求方式：POST

请求内容：需要Cookie

address:text

 

返回内容：

{"error_code":431,"message":"用户名不存在","data":None}

{"error_code": 433, "message": "地址长度应小于40个字符", "data": None}

{"error_code": 200, "message": "地址修改成功", "data": None}

 

### **7.修改生日**

请求地址：/user/modifyBirthday

请求方式：POST

请求内容：需要Cookie

birthday:text

The format of birthday is"YYYY-MM-DD"

 

返回内容：

{"error_code":431,"message":"用户名不存在","data":None}

{"error_code": 433, "message": "昵称长度应小于40个字符", "data": None}

{"error_code": 200, "message": "生日修改成功", "data": None}

 

### **8.修改性别**

请求地址：/user/modifyGender

请求方式：POST

请求内容：需要Cookie

gender:text

gender has a limited value to '男' ,'女' or ‘保密’

 

返回内容：

{"error_code":431,"message":"用户名不存在","data":None}

{"error_code": 433, "message": "性别错误", "data": None}

{"error_code": 200, "message": "性别修改成功", "data": None}

 

### **9.修改昵称**

请求地址：/user/modifyNickname

请求方式：POST

请求内容：需要Cookie

nickname:text

 

返回内容：

{"error_code":431,"message":"用户名不存在","data":None}

{"error_code": 433, "message": "昵称长度应小于20个字符，且不能为空", "data": None}

{"error_code": 200, "message": "昵称修改成功", "data": None}

 

### **10.修改头像**

请求地址：/user/modifyProfile

请求方式：POST

请求内容：需要Cookie

profile:file

 

返回内容：

{"error_code":431,"message":"用户名不存在","data":None}

{"error_code": 200, "message": "头像修改成功", "data": None}

 

### **11.修改签名**

请求地址：/user/modifySignature

请求方式：POST

请求内容：需要Cookie

signature:text

 

返回内容：

{"error_code":431,"message":"用户名不存在","data":None}

{"error_code": 433, "message": "签名长度应小于30个字符", "data": None}

{"error_code": 200, "message": "签名修改成功", "data": None}

 

### **12.获取地址**

请求地址：/user/getAddress

请求方式：POST

请求内容：需要Cookie

 

返回内容：

{"error_code":441,"message":"用户名不存在","data":None}

{"error_code": 200, "message": "获取地址成功", "data": address}

 

### **13.获取生日**

请求地址：/user/getBirthday

请求方式：POST

请求内容：需要Cookie

 

返回内容：

{"error_code":441,"message":"用户名不存在","data":None}

{"error_code": 200, "message": "获取生日成功", "data": birthday}

 

### **14.获取性别**

请求地址：/user/getGender

请求方式：POST

请求内容：需要Cookie

 

返回内容：

{"error_code":441,"message":"用户名不存在","data":None}

{"error_code": 200, "message": "获取性别成功", "data": gender}

 

### **15.获取昵称**

请求地址：/user/getNickname

请求方式：POST

请求内容：需要Cookie

 

返回内容：

{"error_code":441,"message":"用户名不存在","data":None}

{"error_code": 200, "message": "获取昵称成功", "data": nickname}

 

### **16.获取头像**

获取用户头像相对路径。

 

请求地址：/user/getProfile

请求方式：POST

请求内容：需要Cookie

 

返回内容：

{"error_code":441,"message":"用户名不存在","data":None}

{"error_code": 200, "message": "获取头像路径成功", "data": profile_path}

 

### **17.获取签名**

请求地址：/user/getSignature

请求方式：POST

请求内容：需要Cookie

 

返回内容：

{"error_code":441,"message":"用户名不存在","data":None}

{"error_code": 200, "message": "获取签名成功", "data": signature}

 

## **三、博客API**

博客API都以 /blog/ 开头，包括发布和获取博客等功能。

 

博客包括发布博客的用户，发布时间，文本内容字段。

图片包括图片所属的博客，图片编号，图片字段。

### **1.发布博客**

请求地址：/blog/release_blog

请求方式：POST

请求内容：需要Cookie

content:text

pictures:file

pictures:file

...

 

You may attach several pictures in one post.

 

返回内容：

{"error_code":431,"message":"用户名不存在","data":None}

{"error_code": 200, "message": "博客发布成功", "data": None}

 

### **2.获取博客**

请求地址：/user/getBlog

请求方式：POST

请求内容：需要Cookie

 

返回内容：

{"error_code":441,"message":"用户名不存在","data":None}

{"error_code": 200, "message": "获取博客成功", "data": data}

 

Here data is a dictionary, its key is the release time(str) of the blog.

And its value is also a dict {‘content’:content,'pictures':picture_paths}

 

e.g.


```python
{

    "error_code": 200, 

    "message": "\u83b7\u53d6\u535a\u5ba2\u6210\u529f", 

    "data": 

    {	

        "2020-10-10 16:18:31": {"content": "test", "pictures": []}, 

        "2020-10-10 16:19:45": {"content": "test", "pictures": ["blog_images/bid2_pid0.jpg"]},

        "2020-10-10 16:20:09": {"content": "test", "pictures": ["blog_images/bid3_pid0.jpg", "blog_images/bid3_pid1.jpg"]}

    }

}
```

