import facebook
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from users import models as users_model
from .auth_providers import FacebookAuth, InvalidAccessToken
from .serializers import LoginSerializer, SocialLoginSerializer


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


class FacebookLoginView(APIView):

    def post(self, request):
        serializer = SocialLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            provider = serializer.validated_data['provider']
            access_token = serializer.validated_data['access_token']

            if provider != 'facebook':
                raise APIException('invalid provider=[%s]' % provider,
                                   code=status.HTTP_400_BAD_REQUEST)

            # verify token
            FacebookAuth.verify_token(access_token=access_token)

            # get email address from facebook
            try:
                graph = facebook.GraphAPI(access_token=access_token, version='2.1')
                me = graph.get_object('me', fields='email,name')
            except facebook.GraphAPIError as e:
                raise InvalidAccessToken(e.message)

            me['access_token'] = access_token

            # create a MyUser with email and a Token
            user, does_user_created = users_model.MyUser.objects.get_or_create(email=me['email'])
            token, does_token_created = Token.objects.get_or_create(user=user)

            return Response(data={'token': token.key, 'user': me})
