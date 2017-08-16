#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import LoginView, LoginWithFacebookTokenView

urlpatterns = [
    url(r'login', LoginView.as_view()),
    url(r'facebook', LoginWithFacebookTokenView.as_view()),
]