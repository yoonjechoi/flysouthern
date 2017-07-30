#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework.test import APITestCase
from rest_framework import status
from .factories import MyUserFactory


class MyUserTest(APITestCase):

    @staticmethod
    def create_user(email, password):
        user = MyUserFactory.build(email=email)
        user.set_password(password)
        user.save()
        return user

    def test_user_login(self):
        # Given:
        email = 'user1@company.com'
        password = 'mysecret'
        MyUserTest.create_user(email, password)

        # When:
        result = self.client.login(email=email, password=password)

        # Then:
        self.assertTrue(result)
