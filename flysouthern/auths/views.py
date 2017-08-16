import facebook
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users import models as users_model
from .auth_providers import InvalidAccessToken
from .serializers import LoginSerializer, FacebookLoginSerializer


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = users_model.MyUser.objects.get(email=email)
                if not user.check_password(password):
                    return Response(serializer,
                                    status=status.HTTP_401_UNAUTHORIZED)

            except users_model.MyUser.DoesNotExist as e:
                return Response("A user with Email %s DOES NOT exist." % email,
                                status=status.HTTP_401_UNAUTHORIZED)

            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist as e:
                return Response("token is not assigned for the user, %s. "
                                "Please refresh a token." % email,
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(data={"token": token.key}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginWithFacebookTokenView(APIView):
    def post(self, request):
        '''

        response format

        {
            'user': {
                'email': 'fake_user_1@example.com',
                'name': 'fake-user-1',
                'access_token': 'it is my facebook test token'
                },

            'token': 'd6804f767e869807e994e6b1673447c5ba8d6ece'
        }
        '''

        serializer = FacebookLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        _ = request.data['provider']
        access_token = request.data['access_token']

        try:
            graph = facebook.GraphAPI(access_token=access_token, version='2.1')

            # verify access_token using facebook token debug api
            result = graph.debug_access_token(access_token,
                                              settings.FACEBOOK_APP_ID,
                                              settings.FACEBOOK_APP_SECRET)

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

                # get email address from facebook

            me = graph.get_object('me', fields='email,name')

        except facebook.GraphAPIError as e:
            raise InvalidAccessToken(e.message)

        me['access_token'] = access_token

        # create a MyUser with email and a Token
        user, does_user_created = users_model.MyUser.objects.get_or_create(email=me['email'])
        token, does_token_created = Token.objects.get_or_create(user=user)

        return Response(data={'token': token.key, 'user': me})
