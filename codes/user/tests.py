from django.test import TestCase
from user.models import  VerificationCode
import random
import string
import json
# 发送邮件
#from django.test.utils import override_settings

#@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')

# Create your tests here.
class TestRegister(TestCase):

    def setUp(self):

        self.init_user()
        print("--------------开始测试--------------")

    def tearDown(self):

        print("--------------测试结束--------------")

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

    def test_register_illegal_username(self):
        # 不合法用户名

        #用户名为空
        print("--------测试空用户名--------")
        self.user['username'] = ""
        error = self.template_test()
        assert error == 403, "error code = %d"%(error)
        #用户名过长
        print("--------测试长用户名--------")
        i = random.randint(21, 30)
        self.user['username'] = ''.join(random.sample(string.ascii_letters + string.digits + "!@#$%^&*()?><{}[]", i))
        error = self.template_test()
        assert error == 403, "error code = %d"%(error)

    def test_register_illegal_password(self):
        # 不合法密码

        # 密码过短
        i = random.randint(0, 5)
        print("--------测试短密码--------")
        self.user['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i))
        error = self.template_test()
        assert error == 403, "error code = %d"%(error)
        # 密码过长
        print("--------测试长密码--------")
        i = random.randint(21, 30)
        self.user['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i))
        error = self.template_test()
        assert error == 403, "error code = %d"%(error)
        # 密码含有违规字符
        print("--------测试违规密码--------")
        i = random.randint(1, 30)
        self.user['password'] = ''.join(random.sample(string.ascii_letters + string.digits, i - 1) + random.sample("!@#$%^&*()?><{}[]", 1))
        error = self.template_test()
        assert error == 403, "error code = %d"%(error)

    def test_register_illigal_rpassword(self):
        # 不合法重输入密码

        print("--------测试不合法的重输入密码--------")
        # 去掉开头字符
        self.user['r_password'] = self.user['password'][1: ]
        error = self.template_test()
        assert error == 402, "error code = %d"%(error)

    def test_register_wrong_code(self):
        # 验证码错误

        error = self.template_test(code_correct = False)
        assert error == 402, "error code = %d"%(error)

    def test_register_email_conflict(self):
        # 邮箱冲突
        # 即发送验证码的邮箱和注册表单中的邮箱不同

        print("--------测试错误电子邮件--------")
        error = self.template_test(email_correct = False)
        assert error == 402, "error code = %d"%(error)

    def test_register_illegal_email(self):
        # 电子邮件格式错误

        print("--------测试违规电子邮件--------")
        self.user['email'] = "17307130121fudan.edu.cn"
        error = self.template_test()
        assert error == 403, "error code = %d"%(error)
        self.user['email'] = "17307130121@fudan.cn"
        error = self.template_test()
        assert error == 403, "error code = %d"%(error)
        self.user['email'] = "17307130121@fudan.comcn"
        error = self.template_test()
        assert error == 403, "error code = %d"%(error)

    # 重名检测
    def test_register_duplicate_username(self):

        print("--------正常注册--------")

        error = self.template_test()
        assert error == 200, "error code = %d"%(error)

        # 检测重名
        print("--------重名测试--------")
        self.user['email'] = "17307130056@fudan.edu.cn"
        error = self.template_test()
        assert error == 401, "error code = %d"%(error)

    # 重复电子邮件检测
    def test_register_duplicate_email(self):

        print("--------正常注册--------")
        error = self.template_test()
        assert error == 200, "error code = %d"%(error)

        # 检测重复电子邮件
        print("--------重复电子邮件测试--------")
        self.user['username'] = "szy"
        error = self.template_test()
        assert error == 401, "error code = %d"%(error)

    # 注册时发送表单的模板
    def template_test(self, code_correct = True, email_correct = True):
        # 注册时的测试模板
        # Arguments:
        #     code_correct:<bool>, email_correct:<bool>
        # Return:
        #     error code<int>

        print("注册信息为：", self.user)

        email = self.user['email']
        # 发送邮件
        response = self.client.post('/user/sendRegisterCode', {"email" : email})
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