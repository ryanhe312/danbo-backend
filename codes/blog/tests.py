from django.test import TestCase
from user.models import  User
from django.contrib.auth.hashers import make_password
import json

# Create your tests here.

class TestBlog(TestCase):
    # 博客测试
    # release_blog...
    # get_blog...

    def setUp(self):

        # 新建用户
        password = make_password("xingshuhao990729")
        User.objects.create(username = "xsh",password = password,email = "17307130121@fudan.edu.cn")
        password = make_password("sheeeep")
        User.objects.create(username = "szy",password = password,email = "17307130056@fudan.edu.cn")
        print("--------------测试博客功能-------------")

    def tearDown(self):

        print("--------------测试结束-------------")

        return super().tearDown()

    def test_release_blogs(self):

        print("--------发布博客测试--------")
        content = "这是第一条博客"
        error, data = self.release_blog("xsh", content)
        assert error == 200, "error code = %d"%(error)

        content = "这是第二条博客，今天有点冷。"
        pictures = [open('C:/Users/super/Desktop/美图/头像.jpg', 'rb')]
        error, data = self.release_blog("xsh", content, pictures)
        assert error == 200, "error code = %d"%(error)

        content = "这是第三条博客，想摸鱼打游戏"
        pictures = [open('C:/Users/super/Desktop/美图/头像.jpg', 'rb'), open('C:/Users/super/Desktop/美图/loble/66601726_p2_master1200.jpg', 'rb')]
        error, data = self.release_blog("xsh", content, pictures)
        assert error == 200, "error code = %d"%(error)
        pictures = [open('C:/Users/super/Desktop/美图/头像.jpg', 'rb'), open('C:/Users/super/Desktop/美图/loble/66601726_p2_master1200.jpg', 'rb')]
        error, data = self.release_blog("szy", content, pictures)
        assert error == 200, "error code = %d"%(error)

        print("--------获取博客测试--------")
        error, data = self.get_blog("xsh")
        assert error == 200, "error code = %d"%(error)

        self.process_blog(data, "xsh")
        error, data = self.get_blog("szy")
        assert error == 200, "error code = %d"%(error)
        self.process_blog(data, "szy")

    def process_blog(self, blog_dict, username):

        print("博客列表：")
        i = 1
        for key in blog_dict.keys():
            print("第%d条博客， 发布者:%s"%(i, username))
            print("发布时间：", key)
            content, pictures = blog_dict[key]
            print("正文内容：\n", content)
            for p in pictures:
                print("博客图片：", p)
            print()
            i += 1

    def release_blog(self, username, content, pictures = []):
        request = {
            'username':username,
            'content':content,
            'pictures':pictures
            }

        response = self.client.post('/blog/release', request)
        cont = json.loads(response.content)

        return cont['error_code'], cont['data']

    def get_blog(self, username):

        request = {
            'username':username,
            }

        response = self.client.post('/blog/getBlog', request)
        content = json.loads(response.content)

        return content['error_code'], content['data']