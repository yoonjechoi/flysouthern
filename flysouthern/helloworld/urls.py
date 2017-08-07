#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from helloworld import views as helloworld_views

urlpatterns = [
    url(r'helloworld', helloworld_views.hello_world),
    url(r'hellouser', helloworld_views.hello_authenticated_user),
]
