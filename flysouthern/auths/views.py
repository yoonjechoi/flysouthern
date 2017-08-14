from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer

from users import models as users_model


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
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
