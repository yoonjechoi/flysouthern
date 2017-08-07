#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework.test import APITestCase
from rest_framework import status
from .factories import MyUserFactory

from django.contrib.auth import authenticate, login


class MyUserTest(APITestCase):

    @staticmethod
    def create_user(email, password):
        user = MyUserFactory.build(email=email)
        user.set_password(password)
        user.save()
        return user

    def test_authenticate_with_email_passwod(self):
        # Given:
        email = 'user1@company.com'
        password = 'mysecret'
        user = MyUserTest.create_user(email, password)

        # When:
        authenticated_user = authenticate(email=email, password=password)

        # Then:
        self.assertEqual(user, authenticated_user)

    def test_client_login_with_email_passwod(self):
        # Given:
        email = 'user1@company.com'
        password = 'mysecret'
        MyUserTest.create_user(email, password)

        # When:
        result = self.client.login(email=email, password=password)

        # Then:
        self.assertTrue(result)
