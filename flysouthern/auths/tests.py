#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest.mock import patch

from django.conf import settings
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from flysouthern.mixin.tests import MyUserMixin
from users.factories import MyUserFactory
from users.models import MyUser


class AuthsTest(MyUserMixin, APITestCase):
    def test_login(self):
        # Given:
        email = 'user1@company.com'
        password = 'mysecret'
        user, token = AuthsTest.create_user(email=email, password=password)

        # When:
        response = self.client.post('/auth/login',
                                  {'email': email,
                                   'password': password})

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['token'], token.key)

    def test_authenticated_api(self):
        # Given:
        # Create a user and a token with given information
        email = 'user1@company.com'
        password = 'mysecret'
        user, token = AuthsTest.create_user(email=email, password=password)

        # When:
        headers = {'HTTP_AUTHORIZATION': 'Token %s' % token.key}
        response = self.client.get('/test/hellouser', **headers)

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FacebookLoginTest(MyUserMixin, APITestCase):
    @classmethod
    def mock_graph_api(self, MockGraphAPI):
        MockGraphAPI.return_value.debug_access_token.return_value = {
            "data": {
                "app_id": settings.FACEBOOK_APP_ID,
                "application": settings.FACEBOOK_APP_NAME,
                "is_valid": True,
                "scopes": [
                    "email",
                ],
            }
        }

        MockGraphAPI.return_value.get_object.return_value = {
            "name": "user0",
            "email": "user0@company.com"
        }

    @patch('facebook.GraphAPI', autospec=True)
    def test_first_login_with_facebook_access_token(self, MockGraphAPI):
        # Given:
        facebook_access_token = 'it is my facebook test token'
        user_count_before_login = MyUser.objects.count()

        MockGraphAPI.return_value.debug_access_token.return_value = {
            "data": {
                "app_id": settings.FACEBOOK_APP_ID,
                "application": settings.FACEBOOK_APP_NAME,
                "is_valid": True,
                "scopes": [
                    "email",
                ],
            }
        }

        MockGraphAPI.return_value.get_object.return_value = {
            "name": "fake-user-1",
            "email": "fake_user_1@example.com"
        }

        # When:
        response = self.client.post('/auth/facebook',
                                    {'provider': 'facebook',
                                     'access_token': facebook_access_token})

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = Munch(response.data)

        user = MyUser.objects.get(email=response_data.user['email'])
        token = Token.objects.get(key=response_data.token)

        user_count_after_login = MyUser.objects.count()
        token_count_after_login = Token.objects.count()

        self.assertEqual(user_count_before_login + 1, user_count_after_login)
        self.assertEqual(token_count_after_login, user_count_after_login)
        self.assertEqual(token.user, user)

    @patch('facebook.GraphAPI', autospec=True)
    def test_existing_user_login_with_facebook_access_token(self, MockGraphAPI):
        # Given:
        MyUserFactory.reset_sequence(0)
        facebook_access_token = 'it is my facebook test token'
        user, _token = self.create_user()
        token = Token.objects.get(user=user)
        user_count_before_login = MyUser.objects.count()

        self.mock_graph_api(MockGraphAPI)

        # When:
        response = self.client.post('/auth/facebook',
                                    {'provider': 'facebook',
                                     'access_token': facebook_access_token})

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = Munch(response.data)

        user_count_after_login = MyUser.objects.count()

        self.assertEqual(user_count_before_login, user_count_after_login)
        self.assertEqual(response_data.token, token.key)
