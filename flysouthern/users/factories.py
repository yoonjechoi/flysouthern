#!/usr/bin/python
# -*- coding: utf-8 -*-

import factory
from .models import MyUser

class MyUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = MyUser

    email = factory.sequence(lambda n: 'user%d@company.com' % n)
    password = 'mysecretpassword'
    username = factory.sequence(lambda n: 'user%d' % n)


