from django.test import TestCase
from user.models import  User,Follow
from django.contrib.auth.hashers import make_password
import json

# Create your tests here.

class TestBlog(TestCase):
    # 博客测试
    # release_blog...
    # get_blog...
    # refresh_blogs...
    # get_likes...
    # give_like...
    # cancel_like...
    # get_comments...
    # comment...
    # repost_blog

    def setUp(self):

        # 新建用户
        password = make_password("xingshuhao990729")
        user1 = User.objects.create(username = "xsh",password = password,email = "17307130121@fudan.edu.cn")
        password = make_password("123456")
        user2 = User.objects.create(username = "xsh1",password = password,email = "17307130122@fudan.edu.cn")
        password = make_password("123456")
        user3 = User.objects.create(username = "xsh2",password = password,email = "17307130123@fudan.edu.cn")
        password = make_password("123456")
        user4 = User.objects.create(username = "xsh3",password = password,email = "17307130124@fudan.edu.cn")
        self.client.cookies['username'] = "xsh"
        Follow.objects.create(from_user=user1, to_user=user2)
        Follow.objects.create(from_user=user2, to_user=user1)
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
        #pictures = [open('C:/Users/super/Desktop/美图/头像.jpg', 'rb')]
        error, data = self.release_blog("xsh", content)
        assert error == 200, "error code = %d"%(error)

        content = "这是第三条博客，想摸鱼打游戏"
        #pictures = [open('C:/Users/super/Desktop/美图/头像.jpg', 'rb'), open('C:/Users/super/Desktop/美图/loble/66601726_p2_master1200.jpg', 'rb')]
        error, data = self.release_blog("xsh", content)
        assert error == 200, "error code = %d"%(error)
        #pictures = [open('C:/Users/super/Desktop/美图/头像.jpg', 'rb'), open('C:/Users/super/Desktop/美图/loble/66601726_p2_master1200.jpg', 'rb')]
        error, data = self.release_blog("xsh1", content)
        assert error == 200, "error code = %d"%(error)

        print("--------获取博客测试--------")
        error, data = self.get_blog("xsh")
        assert error == 200, "error code = %d"%(error)

        self.process_blog(data)
        error, data = self.get_blog("xsh1")
        assert error == 200, "error code = %d"%(error)
        self.process_blog(data)

        print("--------点赞博客测试--------")
        self.client.cookies['username'] = "xsh"
        error, data = self.give_like(1)
        assert error == 200, "error code = %d"%(error)

        error, data = self.give_like(3)
        assert error == 200, "error code = %d"%(error)

        error, data = self.give_like(4)
        assert error == 200, "error code = %d"%(error)

        print("--------评论博客测试--------")
        error, data = self.comment(1,"想摸鱼")
        assert error == 200, "error code = %d"%(error)

        error, data = self.comment(4,"想摸鱼")
        assert error == 200, "error code = %d"%(error)

        self.client.cookies['username'] = "xsh1"
        error, data = self.comment(1,"摸！")
        self.client.cookies['username'] = "xsh3"
        error, data = self.comment(1,"摸+1！")
        error, data = self.give_like(1)
        self.client.cookies['username'] = "xsh"
        assert error == 200, "error code = %d"%(error)

        print("--------转发博客测试--------")
        error, data = self.repost_blog(1,"那我就摸了")
        assert error == 200, "error code = %d"%(error)

        self.client.cookies['username'] = "xsh1"
        error, data = self.repost_blog(5,"可以")
        assert error == 200, "error code = %d"%(error)

        self.client.cookies['username'] = "xsh"
        error, data = self.refresh_blogs()
        assert error == 200, "error code = %d"%(error)

        self.process_blog(data)

    def process_blog(self, blogs):

        for id, blog in blogs.items():
            print("--------------------------------------------")
            error, likes = self.get_likes(id)
            assert error == 200, "error code = %d"%(error)

            error, comments = self.get_comments(id)
            assert error == 200, "error code = %d"%(error)
            print("发布时间：%s"%(blog['time']))
            user = False
            i = 0
            for i in range(len(blog['users'])):
                u = blog['users'][i]
                c = blog['contents'][i]
                if user == False:
                    user = True
                    print("发布者：%s"%(u))

                for j in range(i):
                    print("\t", end = '')
                print("\t发布者：%s"%(u))

                for j in range(i):
                    print("\t", end = '')
                print("\t内容：%s"%(c))

            i += 1
            for j in range(i):
                print("\t", end = '')
            print("\t发布者：%s"%(blog['origin_user']))
            
            for j in range(i):
                print("\t", end = '')
            print("\t内容：%s"%(blog['origin_content']))

            print("点赞：%d个\n\t"%(len(likes)))
            for like in likes:
                print("\t%s"%(like))

            print("评论：%d条\n"%(len(comments)))
            for c, cmt in comments.items():
                print("\t评论时间：%s 评论者：%s"%(cmt['time'], cmt['username']))
                print("\t\t", cmt['content'])

    def release_blog(self, username, content, pictures = []):
        self.client.cookies['username'] = username
        request = {
            'content':content,
            'pictures':pictures
            }

        response = self.client.post('/blog/releaseBlog', request)
        cont = json.loads(response.content)

        return cont['error_code'], cont['data']

    def get_blog(self, username):

        request = {
            'username':username,
            }

        response = self.client.post('/blog/getBlog', request)
        content = json.loads(response.content)

        return content['error_code'], content['data']

    def give_like(self, blog):

        request = {
            'blog_id': blog
            }

        response = self.client.post('/blog/giveLike', request)
        content = json.loads(response.content)

        return content['error_code'], content['data']

    def cancel_like(self, blog):

        request = {
            'blog_id': blog
            }

        response = self.client.post('/blog/cancelLike', request)
        content = json.loads(response.content)

        return content['error_code'], content['data']

    def comment(self, blog, cont):

        request = {
            'blog_id': blog,
            'content': cont
            }

        response = self.client.post('/blog/comment', request)
        content = json.loads(response.content)

        return content['error_code'], content['data']

    def repost_blog(self, blog, comment):

        request = {
            'blog_id': blog,
            'content': comment
            }

        response = self.client.post('/blog/repostBlog', request)
        content = json.loads(response.content)

        return content['error_code'], content['data']

    def get_comments(self, blog):

        request = {
            'blog_id': blog
            }

        response = self.client.post('/blog/getComments', request)
        content = json.loads(response.content)

        return content['error_code'], content['data']

    def get_likes(self, blog):

        request = {
            'blog_id': blog
            }

        response = self.client.post('/blog/getLikes', request)
        content = json.loads(response.content)

        return content['error_code'], content['data']

    def refresh_blogs(self):

        request = {}

        response = self.client.post('/blog/refreshBlogs', request)
        content = json.loads(response.content)

        return content['error_code'], content['data']