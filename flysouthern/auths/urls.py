#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import LoginView, FacebookLoginView

urlpatterns = [
    url(r'login', LoginView.as_view()),
    url(r'facebook', FacebookLoginView.as_view()),
]