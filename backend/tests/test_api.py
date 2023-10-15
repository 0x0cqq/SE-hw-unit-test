import unittest

from django.test import Client, TestCase
from django.urls import reverse

from user import views as user_views
from user.models import User
from utils.jwt import encrypt_password


class APITestCase(TestCase):

    def setUp(self):
        user = User(username="testuser", password=encrypt_password(str("testuser")),
                    nickname="test", mobile="+86.123456789012", magic_number=0, url="https://baidu.com")
        user.save()
        self.client = Client()

    def test_login(self):
        """
        使用错误的信息进行登录，检查返回值为失败
        """

        # 错误的用户名
        data = {"username": "123", "password": "testuser"}
        response = self.client.patch(
            reverse(user_views.login),
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid credentials")
        self.assertEqual(response.status_code, 401)

        # 错误的密码
        data = {"username": "testuser", "password": "123"}
        response = self.client.patch(
            reverse(user_views.login),
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid credentials")
        self.assertEqual(response.status_code, 401)

        """
        使用正确的信息进行登录，检查返回值为成功
        """
        data = {"username": "testuser", "password": "testuser"}
        response = self.client.patch(
            reverse(user_views.login),
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)

        """
        进行登出，检查返回值为成功
        """

        header = {"Authorization": json_data['jwt']}

        response = self.client.patch(
            reverse(user_views.logout),
            content_type="application/json",
            headers=header
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        """
        Example: 使用错误信息进行注册，检查返回值为失败

        这里的错误和返回码是在还没有实现注册参数校验的情况下的返回值，
        在完成register_params_check后，你需要修改这里的错误信息和返回码
        """
        data = {"username": "123", "password": "21321"}
        response = self.client.post(
            reverse(user_views.register_user),
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid arguments: username")
        self.assertEqual(response.status_code, 400)

        """
        使用正确的信息进行注册，检查返回值为成功
        """

        data = {"username": "testuser123", "password": "TestUser123_", "nickname": "test",
                "mobile": "+86.123456789012", "url": "https://baidu.com", "magic_number": 0}
        response = self.client.post(
            reverse(user_views.register_user),
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)

        """
        使用正确注册信息进行登录，检查返回值为成功
        """

        data = {"username": "testuser123", "password": "TestUser123_"}
        response = self.client.patch(
            reverse(user_views.login),
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        未登录直接登出
        """
        response = self.client.patch(
            reverse(user_views.logout),
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "User must be authorized.")
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
