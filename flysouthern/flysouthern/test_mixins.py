#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework.authtoken.models import Token

from users import factories as users_factory


class MyUserMixin(object):
    @classmethod
    def create_user(cls, email=None, password=None, token_key=None):
        if not email:
            email = "user@example.com"

        if password:
            user = users_factory.MyUserFactory.build(email=email)
            user.set_password(password)
            user.save()

        else:
            user = users_factory.MyUserFactory.create(email=email)

        token = Token.objects.create(user=user, key=token_key)

        return user, token

    @classmethod
    def create_users(cls, number_of_users):
        email_format = 'user{number}@example.com'
        password_format = 'mysecretpassword{number}'

        user_list = []
        for i in range(1, number_of_users + 1):
            email = email_format.format(number=i)
            password = password_format.format(number=i)
            user_list.append(cls.create_user(email, password=password))

        return user_list




