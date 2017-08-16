#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from django.conf import settings
from munch import Munch
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.factories import MyUserFactory
from users.models import MyUser
from flysouthern.test_mixins import MyUserMixin
from .auth_providers import FacebookAuth


class AuthsTest(MyUserMixin, APITestCase):
    def test_login(self):
        # Given:
        email = 'user1@company.com'
        password = 'mysecret'
        user, token = AuthsTest.create_user(email, password)

        # When:
        response = self.client.post('/auth/login',
                                  {'email': email,
                                   'password': password})

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_api(self):
        # Given:
        # Create a user and a token with given information
        email = 'user1@company.com'
        password = 'mysecret'
        user, token = AuthsTest.create_user(email, password)

        # When:
        headers = {'HTTP_AUTHORIZATION': 'Token %s' % token.key}
        response = self.client.get('/test/hellouser', **headers)

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FacebookLoginTest(MyUserMixin, APITestCase):

    # For the purpose of testing
    USER_ACCESS_TOKEN = access_token = 'EAABf7eOV5o4BAIKltVHFeInyFl8vu22lHJAvUT2cKX4BaJIZALfMln15BHI8HDckhoYyOJloEMYkQwlawLJSnCiK5sOF8xUL7pEfsuNJtSgvIRO6pkYYOJOhSgEZC3qGULwDUbtQ6bskamLC7xdeZBt64P7rZAwZD'

    def test_first_login_with_facebook(self):
        # Given:
        before_user_count = MyUser.objects.count()

        # When:
        response = self.client.post('/auth/facebook',
                                    {'provider': 'facebook', 'access_token': self.USER_ACCESS_TOKEN})

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        after_user_count = MyUser.objects.count()
        response_data = Munch(response.data)

        user = MyUser.objects.get(email=response_data.user['email'])
        token = Token.objects.get(key=response_data.token)

        self.assertEqual(before_user_count + 1, after_user_count)
        self.assertEqual(token.user, user)

    def test_existing_user_login_with_facebook(self):
        # Given: an user who logged in with facebook in the past
        email = 'yoonjechoi@gmail.com'
        user = self.create_user(email=email)
        before_user_count = MyUser.objects.count()

        # When:
        response = self.client.post('/auth/facebook',
                                    {'provider': 'facebook', 'access_token': self.USER_ACCESS_TOKEN})

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        after_user_count = MyUser.objects.count()

        response_data = Munch(response.data)

        user = MyUser.objects.get(email=response_data.user['email'])
        token = Token.objects.get(key=response_data.token)

        self.assertEqual(before_user_count, after_user_count)
        self.assertEqual(token.user, user)
