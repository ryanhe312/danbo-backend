from django.test import TestCase
from user.models import  User, VerificationCode
from django.contrib.auth.hashers import make_password
import random
import string
import json
# 发送邮件
#from django.test.utils import override_settings

#@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')

# Create your tests here.
class TestRegister(TestCase):
    # 测试注册功能
    #  python manage.py test user.tests.TestRegister
    # register...完成
    # sned_veri_code_register...完成
    # 

    def setUp(self):

        self.init_user()
        print("--------------开始注册测试--------------")

    def tearDown(self):

        print("--------------注册测试结束--------------")

        return super().tearDown()

    def init_user(self):
        # 初始化合法的用户

        self.user = {}

        i = random.randint(1, 20)
        self.user['username'] = ''.join(random.sample(string.ascii_letters + string.digits + "!@#$%^&*()?><{}[]", i))
        #self['username'] = "xsh729"

        i = random.randint(6, 20)
        self.user['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i))
        self.user['r_password'] = self.user['password']

        self.user['email'] = "17307130121@fudan.edu.cn"

    def test_illegal_username(self):
        # 不合法用户名

        #用户名为空
        print("--------测试空用户名--------")
        self.user['username'] = ""
        error = self.run_test()
        assert error == 403, "error code = %d"%(error)
        #用户名过长
        print("--------测试长用户名--------")
        i = random.randint(21, 30)
        self.user['username'] = ''.join(random.sample(string.ascii_letters + string.digits + "!@#$%^&*()?><{}[]", i))
        error = self.run_test()
        assert error == 403, "error code = %d"%(error)

    def test_illegal_password(self):
        # 不合法密码

        # 密码过短
        i = random.randint(0, 5)
        print("--------测试短密码--------")
        self.user['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i))
        error = self.run_test()
        assert error == 403, "error code = %d"%(error)
        # 密码过长
        print("--------测试长密码--------")
        i = random.randint(21, 30)
        self.user['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i))
        error = self.run_test()
        assert error == 403, "error code = %d"%(error)
        # 密码含有违规字符
        print("--------测试违规密码--------")
        i = random.randint(1, 30)
        self.user['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i - 1) + random.sample("!@#$%^&*()?><{}[]", 1))
        error = self.run_test()
        assert error == 403, "error code = %d"%(error)

    def test_illigal_rpassword(self):
        # 不合法重输入密码

        print("--------测试不合法的重输入密码--------")
        # 去掉开头字符
        self.user['r_password'] = self.user['password'][1: ]
        error = self.run_test()
        assert error == 402, "error code = %d"%(error)

    def test_wrong_code(self):
        # 验证码错误

        print("--------测试错误验证码--------")
        error = self.run_test(code_correct = False)
        assert error == 402, "error code = %d"%(error)

    def test_email_conflict(self):
        # 邮箱冲突
        # 即发送验证码的邮箱和注册表单中的邮箱不同

        print("--------测试错误电子邮件--------")
        error = self.run_test(email_correct = False)
        assert error == 402, "error code = %d"%(error)

    def test_illegal_email(self):
        # 电子邮件格式错误

        print("--------测试违规电子邮件--------")
        self.user['email'] = "17307130121fudan.edu.cn"
        error = self.run_test()
        assert error == 403, "error code = %d"%(error)
        self.user['email'] = "17307130121@fudan.cn"
        error = self.run_test()
        assert error == 403, "error code = %d"%(error)
        self.user['email'] = "17307130121@fudan.comcn"
        error = self.run_test()
        assert error == 403, "error code = %d"%(error)

    # 重名检测
    def test_duplicate_username(self):

        print("--------正常注册--------")

        error = self.run_test()
        assert error == 200, "error code = %d"%(error)

        # 检测重名
        print("--------重名测试--------")
        self.user['email'] = "17307130056@fudan.edu.cn"
        error = self.run_test()
        assert error == 401, "error code = %d"%(error)

    # 重复电子邮件检测
    def test_duplicate_email(self):

        print("--------正常注册--------")
        error = self.run_test()
        assert error == 200, "error code = %d"%(error)

        # 检测重复电子邮件
        print("--------重复电子邮件测试--------")
        self.user['username'] = "szy"
        error = self.run_test()
        assert error == 401, "error code = %d"%(error)

    # 注册时发送表单的模板
    def run_test(self, code_correct = True, email_correct = True):
        # 注册时的测试模板
        # Arguments:
        #     code_correct:<bool>, email_correct:<bool>
        # Return:
        #     error code<int>

        print("注册信息为：", self.user)

        email = self.user['email']
        # 发送邮件
        response = self.client.post('/user/sendRegisterCode', {'email' : email})
        content = json.loads(response.content)
        if content['error_code'] != 200:
            return content['error_code']

        # 获得验证码
        record = VerificationCode.objects.filter(email = email)
        code = record[0].code
        # 正确验证码
        input_code = code
        # 错误验证码 
        # 随机选择一位进行更改，进行增加取模操作
        if code_correct == False:
            i = random.randint(0, 3)
            ch = int(input_code[i])
            ch = (ch + random.randint(1, 8)) % 10
            input_code = input_code[ :i] + str(ch) + input_code[i + 1:]

        # 错误邮箱
        #
        if email_correct == False:
            self.user['email'] = "17307130056@fudan.edu.cn"

        print("发送的验证码为：%s, 输入的验证码为：%s"%(code, input_code))

        # 注册
        self.user['code'] = input_code
        response = self.client.post('/user/register', self.user)

        content = json.loads(response.content)
        return content['error_code']

class TestLogin(TestCase):
    # 测试登录功能和修改密码功能
    # python manage.py test user.tests.TestLogin
    # login...完成

    @classmethod
    def setUpClass(cls):

        # 新建两个用户
        password = make_password("xingshuhao990729")
        User.objects.create(username = "xsh",password = password,email = "17307130121@fudan.edu.cn")
        password = make_password("sheeeep")
        User.objects.create(username = "szy",password = password,email = "17307130056@fudan.edu.cn")
        return super().setUpClass()

    def setUp(self):

        self.login = {
            "username": "xsh",
            "password": "xingshuhao990729"
            }
        print("--------------开始登录测试--------------")

    def tearDown(self):

        print("--------------登录测试结束--------------")

        return super().tearDown()

    def test_no_user(self):

        print("登录信息为：", self.login)
        print("--------用户不存在--------")
        self.login['username'] = "xsh729"
        error = self.run_test()
        assert error == 411, "error code = %d"%(error)

    def test_wrong_password(self):

        print("--------密码输入错误--------")
        print("登录信息为：", self.login)
        self.login['password'] = "xsh999999"
        error = self.run_test()
        assert error == 412, "error code = %d"%(error)

        self.login['username'] = "szy"
        self.login['password'] = ""
        print("登录信息为：", self.login)
        error = self.run_test()
        assert error == 412, "error code = %d"%(error)

        self.login['password'] = "sheeeeeeep"
        print("登录信息为：", self.login)
        error = self.run_test()
        assert error == 412, "error code = %d"%(error)

    def run_test(self):

        response = self.client.post('/user/login', self.login)

        content = json.loads(response.content)
        return content['error_code']

class TestModifyPassword(TestCase):
    # 修改密码功能的测试
    # python manage.py test user.tests.TestModifyPassword
    # send_veri_code_login...完成
    # modify_password...完成

    def setUp(self):

        # 新建用户
        password = make_password("xingshuhao990729")
        User.objects.create(username = "xsh",password = password,email = "17307130121@fudan.edu.cn")
        password = make_password("sheeeep")
        User.objects.create(username = "szy",password = password,email = "17307130056@fudan.edu.cn")

        self.modify = {
            "username": "xsh",
            "password": "xsh990729",
            "r_password": "xsh990729",
            "email": "17307130121@fudan.edu.cn"
            }
        print("--------------开始修改密码测试--------------")

    def tearDown(self):

        print("--------------修改密码测试结束--------------")

        return super().tearDown()

    def test_no_user(self):
        # 用户不存在

        print("--------测试不存在用户--------")
        self.modify['username'] = "xxxsh"
        error = self.run_test()
        assert error == 421, "error code = %d"%(error)

    def test_illegal_password(self):
        # 不合法密码

        # 密码过短
        i = random.randint(0, 5)
        print("--------测试短密码--------")
        self.modify['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i))
        error = self.run_test()
        assert error == 423, "error code = %d"%(error)
        # 密码过长
        print("--------测试长密码--------")
        i = random.randint(21, 30)
        self.modify['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i))
        error = self.run_test()
        assert error == 423, "error code = %d"%(error)
        # 密码含有违规字符
        print("--------测试违规密码--------")
        i = random.randint(1, 30)
        self.modify['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i - 1) + random.sample("!@#$%^&*()?><{}[]", 1))
        error = self.run_test()
        assert error == 423, "error code = %d"%(error)

    def test_illigal_rpassword(self):
        # 不合法重输入密码

        print("--------测试不合法的重输入密码--------")
        # 去掉开头字符
        self.modify['r_password'] = self.modify['password'][1: ]
        error = self.run_test()
        assert error == 422, "error code = %d"%(error)

    def test_wrong_code(self):
        # 验证码错误

        error = self.run_test(code_correct = False)
        assert error == 422, "error code = %d"%(error)

    def test_wrong_email(self):
        # 发送验证码的邮箱和注册时的邮箱不同

        print("--------测试错误电子邮件--------")
        self.modify['email'] = "17307130118@fudan.edu.cn"
        error = self.run_test()
        assert error == 422, "error code = %d"%(error)

    def test_illegal_email(self):
        # 电子邮件格式错误

        print("--------测试违规电子邮件--------")
        self.modify['email'] = "17307130121fudan.edu.cn"
        error = self.run_test()
        assert error == 423, "error code = %d"%(error)
        self.modify['email'] = "17307130121@fudan.cn"
        error = self.run_test()
        assert error == 423, "error code = %d"%(error)
        self.modify['email'] = "17307130121@fudan.comcn"
        error = self.run_test()
        assert error == 423, "error code = %d"%(error)

    # 正常修改测试
    def test_normal(self):

        error = self.run_test()
        assert error == 200, "error code = %d"%(error)

        # 重新登录
        # 旧密码
        login = {
            "username": self.modify['username'],
            "password": "xingshuhao990729"
            }

        response = self.client.post('/user/login', login)

        content = json.loads(response.content)
        error = content['error_code']
        assert error == 412, "error code = %d"%(error)

        # 新密码
        login['password'] = self.modify['password']
        response = self.client.post('/user/login', login)

        content = json.loads(response.content)
        error = content['error_code']
        assert error == 200, "error code = %d"%(error)

    def run_test(self, code_correct = True):
        # 修改密码的测试模板
        # Arguments:
        #     code_correct:<bool>, email_correct:<bool>
        # Return:
        #     error code<int>

        email = self.modify['email']
        # 发送邮件
        response = self.client.post('/user/sendLoginCode', {'email' : email})
        content = json.loads(response.content)
        if content['error_code'] != 200:
            print("邮件发送失败")
            return content['error_code']

        # 获得验证码
        record = VerificationCode.objects.filter(email = email)
        code = record[0].code
        # 正确验证码
        input_code = code
        # 错误验证码 
        # 随机选择一位进行更改，进行增加取模操作
        if code_correct == False:
            i = random.randint(0, 3)
            ch = int(input_code[i])
            ch = (ch + random.randint(1, 8)) % 10
            input_code = input_code[ :i] + str(ch) + input_code[i + 1:]

        print("发送的验证码为：%s, 输入的验证码为：%s"%(code, input_code))

        # 修改
        self.modify['code'] = input_code
        response = self.client.post('/user/modifyPwd', self.modify)
        content = json.loads(response.content)
        return content['error_code']
    

class TestInformation(TestCase):
    # 个人资料的修改测试（除头像）
    # python manage.py test user.tests.TestProfile
    # modify_nickname...完成
    # modify_gender...完成
    # modify_birthday...
    # modify_address...
    # modify_signature...

    @classmethod
    def setUpClass(cls):

        password = make_password("xingshuhao990729")
        User.objects.create(username = "xsh",password = password,email = "17307130121@fudan.edu.cn",
                            gender = "男", birthday = "1999-07-29", address = "山东省威海市", 
                            signature = "奔向夜晚")
        return super().setUpClass()

    def setUp(self):

        print("--------------开始个人资料测试--------------")

    def tearDown(self):

        print("--------------个人资料测试结束--------------")

        return super().tearDown()

    def test_nickname(self):

        request = {'username':'xsh'}
        get = "getNickname"
        modify = "modifyNickname"

        print("--------测试昵称--------")
        print("-----获取昵称：用户不存在-----")
        request = {'username':'szy'}
        error, data = self.get_response(get, request)
        assert error == 441, "error code = %d"%(error)

        print("-----获取昵称-----")
        request = {'username':'xsh'}

        error, data = self.get_response(get, request)
        print("用户昵称为", data)
        assert error == 200, "error code = %d"%(error)
        assert data == "游客", "nickname = %s"%(data)

        print("-----修改昵称：用户不存在-----")
        request = {'username':'szy', 'nickname':'x54_729'}
        error, data = self.get_response(modify, request)
        assert error == 431, "error code = %d"%(error)

        print("-----修改昵称：昵称过长-----")
        request = {
            'username':'xsh', 
            "nickname":"测试昵称测试昵称测试昵称测试昵称测试昵称测试昵称"
            }
        error, data = self.get_response(modify, request)
        assert error == 433, "error code = %d"%(error)

        print("-----修改昵称：昵称为空-----")
        request['nickname'] = ""
        error, data = self.get_response(modify, request)
        assert error == 433, "error code = %d"%(error)

        print("-----修改昵称：成功-----")
        request['nickname'] = "x54_729"
        print("昵称修改为", request['nickname'])
        error, data = self.get_response(modify, request)
        assert error == 200, "error code = %d"%(error)

        error, data = self.get_response(get, request)
        assert error == 200, "error code = %d"%(error)
        print("修改后昵称为", data)
        assert data == request['nickname'], "nickname changed = %s"%(data)

    def test_gender(self):

        request = {'username':'xsh'}
        get = "getGender"
        modify = "modifyGender"

        print("--------测试性别--------")
        print("-----获取性别：用户不存在-----")
        request = {'username':'szy'}
        error, data = self.get_response(get, request)
        assert error == 441, "error code = %d"%(error)

        print("-----获取性别-----")
        request = {'username':'xsh'}
        error, data = self.get_response(get, request)
        print("用户性别为", data)
        assert error == 200, "error code = %d"%(error)
        assert data == "男", "gender = %s"%(data)

        print("-----修改性别：用户不存在-----")
        request = {'username':'szy', 'gender':'女'}
        error, data = self.get_response(modify, request)
        assert error == 431, "error code = %d"%(error)

        print("-----修改性别：性别错误-----")
        request = {
            'username':'xsh', 
            'gender': "a"
            }
        error, data = self.get_response(modify, request)
        assert error == 433, "error code = %d"%(error)

        print("-----修改昵称：成功-----")
        request['gender'] = "女"
        print("性别修改为", request['gender'])
        error, data = self.get_response(modify, request)
        assert error == 200, "error code = %d"%(error)

        error, data = self.get_response(get, {'username':'xsh'})
        assert error == 200, "error code = %d"%(error)
        print("修改后性别为", data)
        assert data == request['gender'], "gender changed = %s"%(data)

    def test_birthday(self):

        request = {'username':'xsh'}
        get = "getBirthday"
        modify = "modifyBirthday"

        print("--------测试生日--------")
        print("-----获取生日：用户不存在-----")
        request = {'username':'szy'}
        error, data = self.get_response(get, request)
        assert error == 441, "error code = %d"%(error)

        print("-----获取生日-----")
        request = {'username':'xsh'}
        error, data = self.get_response(get, request)
        print("用户性别为", data)
        assert error == 200, "error code = %d"%(error)
        assert data == "1999-07-29", "gender = %s"%(data)

        print("-----修改生日：用户不存在-----")
        request = {'username':'szy', 'birthday':'1972-07-02'}
        error, data = self.get_response(modify, request)
        assert error == 431, "error code = %d"%(error)

        print("-----修改生日：成功-----")
        request['username'] = 'xsh'
        request['birthday'] = '1972-07-02'
        print("生日修改为", request['birthday'])
        error, data = self.get_response(modify, request)
        assert error == 200, "error code = %d"%(error)

        error, data = self.get_response(get, {'username':'xsh'})
        assert error == 200, "error code = %d"%(error)
        print("修改后生日为", data)
        assert data == request['birthday'], "birthday changed = %s"%(data)

    def test_address(self):

        request = {'username':'xsh'}
        get = "getAddress"
        modify = "modifyAddress"

        print("--------测试地址--------")
        print("-----获取地址：用户不存在-----")
        request = {'username':'szy'}
        error, data = self.get_response(get, request)
        assert error == 441, "error code = %d"%(error)

        print("-----获取地址-----")
        request = {'username':'xsh'}
        error, data = self.get_response(get, request)
        print("用户地址为", data)
        assert error == 200, "error code = %d"%(error)
        assert data == "山东省威海市", "address = %s"%(data)

        print("-----修改地址：用户不存在-----")
        request = {'username':'szy', 'address':'上海市虹口区'}
        error, data = self.get_response(modify, request)
        assert error == 431, "error code = %d"%(error)

        print("-----修改地址：地址过长-----")
        request = {
            'username':'xsh', 
            'address': "测试地址测试地址测试地址测试地址测试地址测试地址测试地址测试地址测试地址测试地址测试地址"
            }
        error, data = self.get_response(modify, request)
        assert error == 433, "error code = %d"%(error)

        print("-----修改地址：成功-----")
        request['address'] = "上海市虹口区"
        print("地址修改为", request['address'])
        error, data = self.get_response(modify, request)
        assert error == 200, "error code = %d"%(error)

        error, data = self.get_response(get, {'username':'xsh'})
        assert error == 200, "error code = %d"%(error)
        print("修改后地址为", data)
        assert data == request['address'], "address changed = %s"%(data)

    def test_signature(self):

        request = {'username':'xsh'}
        get = "getSignature"
        modify = "modifySignature"

        print("--------测试个性签名--------")
        print("-----获取签名：用户不存在-----")
        request = {'username':'szy'}
        error, data = self.get_response(get, request)
        assert error == 441, "error code = %d"%(error)

        print("-----获取签名-----")
        request = {'username':'xsh'}
        error, data = self.get_response(get, request)
        print("用户签名为：", data)
        assert error == 200, "error code = %d"%(error)
        assert data == "奔向夜晚", "signature = %s"%(data)

        print("-----修改签名：用户不存在-----")
        request = {'username':'szy', 'signature':'LEFT SIDE, RIGHT SIDE, YOU ARE KING.'}
        error, data = self.get_response(modify, request)
        assert error == 431, "error code = %d"%(error)

        print("-----修改签名：签名过长-----")
        request = {
            'username':'xsh', 
            'signature': 'LEFT SIDE, RIGHT SIDE, YOU ARE KING.'
            }
        error, data = self.get_response(modify, request)
        assert error == 433, "error code = %d"%(error)

        print("-----修改个性签名：成功-----")
        request['signature'] = "LEFT SIDE, RIGHT SIDE"
        print("个性签名修改为", request['signature'])
        error, data = self.get_response(modify, request)
        assert error == 200, "error code = %d"%(error)

        error, data = self.get_response(get, {'username':'xsh'})
        assert error == 200, "error code = %d"%(error)
        print("修改后个性签名为", data)
        assert data == request['signature'], "signature changed = %s"%(data)

    def get_response(self, url, request):

        response = self.client.post('/user/' + url, request)
        content = json.loads(response.content)
        return content['error_code'], content['data']