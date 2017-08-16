#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class FacebookLoginSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=64)
    access_token = serializers.CharField()
    access_token_secret = serializers.CharField(required=False)