#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
