import unittest

from django.test import TestCase

from utils.register_params_check import register_params_check


class BasicTestCase(TestCase):

    def test_username_missing(self):
        content = {
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("username", False))

    def test_username_invalid_too_short(self):
        content = {
            "username": "a123",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("username", False))

    
    def test_username_invalid_layout(self):
        content = {
            "username": "123abc123",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("username", False))

    def test_password_missing(self):
        content = {
            "username": "abc12345",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("password", False))

    def test_password_invalid_too_short(self):
        content = {
            "username": "abc12345",
            "password": "Abc124*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": 0,
        }
        result = register_params_check(content)
        self.assertEqual(result, ("password", False))

    def test_password_invalid(self):
        content = {
            "username": "abc12345",
            "password": "abc12345",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("password", False))

    def test_mobile_missing(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "url": "https://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("mobile", False))
    
    def test_mobile_wrong_type(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": 123456789012,
            "url": "https://www.google.com",
            "magic_number": 0,
        }
        result = register_params_check(content)
        self.assertEqual(result, ("mobile", False))

    def test_mobile_invalid(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.12345678901",
            "url": "https://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("mobile", False))

    def test_nickname_missing(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("nickname", False))
    
    def test_nickname_wrong_type(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": 123,
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": 0,
        }
        result = register_params_check(content)
        self.assertEqual(result, ("nickname", False))

    def test_url_missing(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("url", False))
    
    def test_url_wrong_type(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": 123,
            "magic_number": 0,
        }
        result = register_params_check(content)
        self.assertEqual(result, ("url", False))

    def test_url_invalid_protocol(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "ftp://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("url", False))

    def test_url_invalid_domain(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.123",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("url", False))

    def test_url_invalid_tag(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.-com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("url", False))
    
    def test_magic_number_invalid_type(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": "0"
        }
        result = register_params_check(content)
        self.assertEqual(result, ("magic_number", False))
    
    def test_magic_number_missing(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012"
        }
        result = register_params_check(content)
        self.assertEqual(result, ("ok", True))

    def test_magic_number_invalid(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": -1
        }
        result = register_params_check(content)
        self.assertEqual(result, ("magic_number", False))

    def test_all_valid(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
            "magic_number": 0
        }
        result = register_params_check(content)
        self.assertEqual(result, ("ok", True))

    def test_magic_number_missing(self):
        content = {
            "username": "abc12345",
            "password": "Abc12345*",
            "nickname": "test",
            "mobile": "+86.123456789012",
            "url": "https://www.google.com",
        }
        result = register_params_check(content)
        self.assertEqual(result, ("ok", True))


if __name__ == "__main__":
    unittest.main()
