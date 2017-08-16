#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import LoginWithEmailPasswordView, LoginWithFacebookTokenView

urlpatterns = [
    url(r'login', LoginWithEmailPasswordView.as_view()),
    url(r'facebook', LoginWithFacebookTokenView.as_view()),
]