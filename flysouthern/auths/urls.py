#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import LoginView
urlpatterns = [
    url(r'auth/login', LoginView.as_view()),
]