#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.factories import MyUserFactory


class AuthsTest(APITestCase):
    @staticmethod
    def create_user(email, password):
        user = MyUserFactory.build(email=email)
        user.set_password(password)
        user.save()

        return user

    def test_login(self):
        # Given:
        email = 'user1@company.com'
        password = 'mysecret'
        user = AuthsTest.create_user(email, password)
        token_key = 'my_access_token'
        Token.objects.create(key=token_key, user=user)

        # When:
        response = self.client.post('/api/auth/login',
                                  {'email': email,
                                   'password': password})

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_api(self):
        # Given:
        # Create a user and a token with given information
        email = 'user1@company.com'
        password = 'mysecret'
        user = AuthsTest.create_user(email, password)

        key = 'my_access_token'
        Token.objects.create(key=key, user=user)

        # When:
        headers = {'HTTP_AUTHORIZATION': 'Token %s' % key}
        response = self.client.get('/test/hellouser', **headers)

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
