#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework.authtoken.models import Token

from users import factories as users_factories


class MyUserMixin(object):
    @classmethod
    def create_user(cls, **kwargs):
        user = users_factories.MyUserFactory.create(**kwargs)
        if 'password' in kwargs:
            user.set_password(kwargs['password'])
            user.save()

        token = Token.objects.create(user=user)
        return user, token

    @classmethod
    def create_users(cls, number_of_users):
        email_format = 'user{number}@example.com'
        password_format = 'mysecretpassword{number}'

        user_list = []
        for i in range(1, number_of_users + 1):
            email = email_format.format(number=i)
            password = password_format.format(number=i)
            user_list.append(cls.create_user(email=email, password=password))

        return user_list




