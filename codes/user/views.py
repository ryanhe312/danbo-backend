from django.shortcuts import render,HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from user.models import  User,VerificationCode
from blog.models import Blog,Picture
from django.core.mail import send_mail
import re
import random
import time
import json

# Create your views here.

def check_password2(password):
    # 检查密码是否合法
    # Arguments:
    #     password<str>
    # Return:
    #     True if the password is valid
    #     False if the password is invalid
    pattern = r'^[0-9a-zA-Z]{6,20}$'
    if re.match(pattern,password):
        return True
    return False

def check_email(email):
    # 检查邮箱是否合法
    # Arguments:
    #     email<str>
    # Return:
    #     True if the email is valid
    #     False if the email is invalid
    pattern=r'^[0-9a-zA-Z_]{0,19}@fudan\.edu\.cn$'
    #pattern=r'^[0-9a-zA-Z_]{0,19}@[0-9a-z]{1,10}(\.[a-z]+)?(\.com|\.net|\.cn){1,3}$'
    if re.match(pattern,email):
        return True
    return False

def generate_veri_code(email):
    # 生成随机的验证码
    # Arguments:
    #     email<str>
    # Return:
    #     code<str>
    code=''
    for i in range(4):
        code+=str(random.randint(0,9))
    record = VerificationCode.objects.filter(email=email)
    timestamp = time.time()
    if record.exists():
        record.update(code=code,timestamp=timestamp)
    else:
        VerificationCode.objects.create(email=email,code=code,timestamp=timestamp)
    return code

def check_veri_code(email,code):
    # 检查验证码是否正确且未过期
    # Arguments:
    #     email<str>,code<str>
    # Return:
    #     True if the verification code is valid
    #     False if the verification code is invalid
    record = VerificationCode.objects.filter(email=email)
    if record.exists():
        true_code = record[0].code
        timestamp = record[0].timestamp
        if code == true_code and time.time()-timestamp < 900:
            return True
    return False

def resgister(request):
    # 用户注册
    # Arguments:
    #     request: It should contains {"username":<str>, "password":<str>,"r_password":<str>, "email":<str>,"code":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content={}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        r_password= request.POST.get('r_password')
        email = request.POST.get('email')
        code = request.POST.get('code')
        print("email = ", email)
        if User.objects.filter(username=username).exists():
            content = {"error_code":401,"message":"用户名已注册","data":None}
        elif not (1 <= len(username) and len(username) <= 20):
            content = {"error_code":403,"message":"用户名长度应在1-20之间","data":None}
        elif User.objects.filter(email=email).exists():
            content = {"error_code":401,"message":"邮箱已注册","data":None}
        elif check_password2(password)==False:
            content = {"error_code": 403, "message": "密码只能由大小写字母，数字组成，且长度应在6-20之间", "data": None}
        elif password != r_password:
            content = {"error_code":402,"message":"两次输入的密码不一致","data":None}
        elif check_email(email)==False:
            content = {"error_code": 403, "message": "邮箱格式不正确", "data": None}
        elif check_veri_code(email,code)==False:
            content = {"error_code": 402, "message": "验证码不正确或已过期", "data": None}
        else:
            content = {"error_code": 200, "message": "注册成功", "data": None}
            password=make_password(password)
            User.objects.create(username=username,password=password,email=email)
    print(content)

    return HttpResponse(json.dumps(content))

    #return render(request,'register.html')

def send_veri_code_register(request):
    # 向用户发送注册验证码
    # Arguments:
    #     request: It should contains {"email":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        if check_email(email) == False:
            content = {"error_code": 403, "message": "邮箱格式不正确", "data": None}
        elif User.objects.filter(email=email).exists():
            content = {"error_code":401,"message":"邮箱已注册","data":None}
        else:
            code =generate_veri_code(email)
            subject = "蛋博注册验证"
            message = "欢迎加入蛋博！您的注册验证码为{}，请在15分钟内输入验证码完成注册，切勿将验证码泄露于他人".format(code)
            send_mail(subject,message,"fudan_danbo@163.com",[email],fail_silently=False)
            content = {"error_code": 200, "message": "邮件发送成功", "data": None}

    #return render(request,'mail.html')
    return HttpResponse(json.dumps(content))

def login(request):
    # 用户登录
    # Arguments:
    #     request: It should contains {"username":<str>, "password":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists() == False:
            content = {"error_code": 411, "message": "用户不存在", "data": None}
        else:
            key = User.objects.get(username=username).password
            if check_password(password,key) == False:
                content = {"error_code": 412, "message": "密码不正确", "data": None}
            else:
                content = {"error_code": 200, "message": "登录成功", "data": None}
    return HttpResponse(json.dumps(content))
    #return render(request,'login.html')

def send_veri_code_login(request):
    # 向用户邮箱发送登录时找回密码的验证码
    # Arguments:
    #     request: It should contains { "email":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        if check_email(email) == False:
            content = {"error_code": 423, "message": "邮箱格式不正确", "data": None}
        elif (User.objects.filter(email=email).exists()) == False:
            content = {"error_code": 422, "message": "该邮箱不是您注册时填写的邮箱", "data": None}
        elif email != User.objects.get(email=email).email:
            content = {"error_code": 422, "message": "该邮箱不是您注册时填写的邮箱", "data": None}
        else:
            code = generate_veri_code(email)
            subject = "蛋博找回密码"
            message = "您的验证码为{}，请在15分钟内输入验证码，切勿将验证码泄露于他人".format(code)
            send_mail(subject, message, "fudan_danbo@163.com", [email], fail_silently=False)
            content = {"error_code": 200, "message": "邮件发送成功", "data": None}
    #return render(request, 'mail.html')
    return HttpResponse(json.dumps(content))

def modify_password(request):
    # 用户修改密码
    # Arguments:
    #     request: It should contains {"username":<str>, "password":<str>,"r_password":<str>, "email":<str>, "code":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        r_password= request.POST.get('r_password')
        email = request.POST.get('email')
        code = request.POST.get('code')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":421,"message":"用户名不存在","data":None}
        elif check_password2(password)==False:
            content = {"error_code": 423, "message": "密码只能由大小写字母，数字组成，且长度应在6-20", "data": None}
        elif password != r_password:
            content = {"error_code":422,"message":"两次输入的密码不一致","data":None}
        elif check_email(email)==False:
            content = {"error_code": 423, "message": "邮箱格式不正确", "data": None}
        elif email != User.objects.get(email=email).email:
            content = {"error_code": 422, "message": "该邮箱不是您注册时填写的邮箱", "data": None}
        elif check_veri_code(email,code)==False:
            content = {"error_code": 422, "message": "验证码不正确或已过期", "data": None}
        else:
            password=make_password(password)
            User.objects.filter(username=username).update(password=password)
            content = {"error_code": 200, "message": "密码修改成功", "data": None}
        print(content)
    return HttpResponse(json.dumps(content))

def modify_signature(request):
    # 用户修改签名
    # Arguments:
    #     request: It should contains {"username":<str>,"signature":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        signature = request.POST.get('signature')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":431,"message":"用户名不存在","data":None}
        elif len(signature)>30:
            content = {"error_code": 433, "message": "签名长度应小于30个字符", "data": None}
        else:
            User.objects.filter(username=username).update(signature=signature)
            content = {"error_code": 200, "message": "签名修改成功", "data": None}
    return HttpResponse(json.dumps(content))

def modify_nickname(request):
    # 用户修改昵称
    # Arguments:
    #     request: It should contains {"username":<str>,"nickname":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":431,"message":"用户名不存在","data":None}
        elif len(nickname)>20 or len(nickname)==0:
            content = {"error_code": 433, "message": "昵称长度应小于20个字符，且不能为空", "data": None}
        else:
            User.objects.filter(username=username).update(nickname=nickname)
            content = {"error_code": 200, "message": "昵称修改成功", "data": None}
    return HttpResponse(json.dumps(content))

def modify_address(request):
    # 用户修改地址
    # Arguments:
    #     request: It should contains {"username":<str>,"address":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        address = request.POST.get('address')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":431,"message":"用户名不存在","data":None}
        elif len(address)>40:
            content = {"error_code": 433, "message": "地址长度应小于40个字符", "data": None}
        else:
            User.objects.filter(username=username).update(address=address)
            content = {"error_code": 200, "message": "地址修改成功", "data": None}
    return HttpResponse(json.dumps(content))

def modify_birthday(request):
    # 用户修改生日
    # Arguments:
    #     request: It should contains {"username":<str>,"birthday":<str>}
    #              The format of birthday is"YYYY-MM-DD" 
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        birthday = request.POST.get('birthday')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":431,"message":"用户名不存在","data":None}
        elif len(birthday)>40:
            content = {"error_code": 433, "message": "生日长度应小于40个字符", "data": None}
        else:
            User.objects.filter(username=username).update(birthday=birthday)
            content = {"error_code": 200, "message": "生日修改成功", "data": None}
    return HttpResponse(json.dumps(content))

def modify_gender(request):
    # 用户修改性别
    # Arguments:
    #     request: It should contains {"username":<str>,"gender":<str>}
    #              gender has a limited value to '男' or '女' or '保密'
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":431,"message":"用户名不存在","data":None}
        elif gender!='男' and gender!='女' and gender != '保密':
            content = {"error_code": 433, "message": "性别错误", "data": None}
        else:
            User.objects.filter(username=username).update(gender=gender)
            content = {"error_code": 200, "message": "性别修改成功", "data": None}
    return HttpResponse(json.dumps(content))

def modify_profile(request):
    # 用户修改头像
    # Arguments:
    #     request: It should contains {"username":<str>,"profile_path":<str> }
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":None}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        profile_path = request.POST.get('profile_path')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":431,"message":"用户名不存在","data":None}
        else:
            User.objects.filter(username=username).update(profile=profile_path)
            content = {"error_code": 200, "message": "头像修改成功", "data": None}
    return HttpResponse(json.dumps(content))

def get_nickname(request):
    # 获取用户昵称
    # Arguments:
    #     request: It should contains {"username":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<str>}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":441,"message":"用户名不存在","data":None}
        else:
            nickname=User.objects.get(username=username).nickname
            content = {"error_code": 200, "message": "获取昵称成功", "data": nickname}
    return HttpResponse(json.dumps(content))

def get_signature(request):
    # 获取用户签名
    # Arguments:
    #     request: It should contains {"username":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<str>}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":441,"message":"用户名不存在","data":None}
        else:
            signature=User.objects.get(username=username).signature
            content = {"error_code": 200, "message": "获取签名成功", "data": signature}
    return HttpResponse(json.dumps(content))

def get_birthday(request):
    # 获取用户生日
    # Arguments:
    #     request: It should contains {"username":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<str>}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":441,"message":"用户名不存在","data":None}
        else:
            birthday=User.objects.get(username=username).birthday
            content = {"error_code": 200, "message": "获取生日成功", "data": str(birthday)}
    return HttpResponse(json.dumps(content))

def get_gender(request):
    # 获取用户性别
    # Arguments:
    #     request: It should contains {"username":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<str>}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":441,"message":"用户名不存在","data":None}
        else:
            gender=User.objects.get(username=username).gender
            content = {"error_code": 200, "message": "获取性别成功", "data": gender}
    return HttpResponse(json.dumps(content))

def get_address(request):
    # 获取用户地址
    # Arguments:
    #     request: It should contains {"username":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<str>}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":441,"message":"用户名不存在","data":None}
        else:
            address=User.objects.get(username=username).address
            content = {"error_code": 200, "message": "获取地址成功", "data": address}
    return HttpResponse(json.dumps(content))

def get_profile_path(request):
    # 获取用户头像路径，注意这里获取的是相对路径，绝对路径为：MEDIA_ROOT + 相对路径
    # MEDIA_ROOT 定义见setting.py
    # Arguments:
    #     request: It should contains {"username":<str>}
    # Return:
    #     An HttpResponse which contains {"error_code":<int>, "message":<str>,"data":<str>}
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            content = {"error_code":441,"message":"用户名不存在","data":None}
        else:
            profile_path=User.objects.get(username=username).profile
            content = {"error_code": 200, "message": "获取头像路径成功", "data": profile_path}
    return HttpResponse(json.dumps(content))


