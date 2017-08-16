#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import facebook
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidAccessToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'invalid access_token error'
    default_code = 'invliad_access_token_error'


class FacebookAuth(object):
    URL_INSPECT_TOKEN = 'https://graph.facebook.com/debug_token?' \
                        'input_token={token_to_inspect}&access_token={app_token}'

    @classmethod
    def verify_token(cls, access_token):
        url = FacebookAuth.URL_INSPECT_TOKEN.format(token_to_inspect=access_token,
                                                    app_token=settings.FACEBOOK_APP_TOKEN)
        response = requests.get(url)
        result = response.json()

        if 'error' in result:
            error = result['error']
            raise InvalidAccessToken(error['message'])

        data = result['data']

        if not data['is_valid']:
            raise InvalidAccessToken(data['error']['message'])

        if data['application'] != settings.FACEBOOK_APP_NAME:
            raise InvalidAccessToken('incorrect application. '
                                     'expect={expect}, actual={actual}'
                                     .format(expect=settings.FACEBOOK_APP_NAME,
                                             actual=data['application']))

        scopes = data['scopes']

        if 'email' not in scopes:
            raise InvalidAccessToken('email is not permitted from facebook.')

        return result

    @classmethod
    def get_email(cls, access_token):
        graph = facebook.GraphAPI(access_token=access_token, version='2.1')
        me = graph.get_object('me', fields='email,name')

        return me
