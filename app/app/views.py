from rest_framework import views
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from api.models import CustomUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from . import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class LoginViewSet(views.APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializers.LoginSerializer)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'detail': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)
        email = authenticate(username=email, password=password)
        if not email:
            return Response({'detail': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=email)
        return Response({'token': token.key}, status=HTTP_200_OK)

class RegisterViewSet(views.APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializers.RegisterSerializer)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        confirmpassword = request.data.get("confirmpassword")

        try:
            validate_email(email)
        except ValidationError:
            return Response({'detail': 'Please enter a valid email'},status=HTTP_400_BAD_REQUEST)

        if email is None or password is None or confirmpassword is None:
            return Response({'detail': 'Please provide all the credentials'},status=HTTP_400_BAD_REQUEST)
        if password != confirmpassword:
            return Response({'detail': 'Mismatch password and confirm password'}, status=HTTP_404_NOT_FOUND)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None
        if user:
            return Response({'detail': 'User already exists'},status=HTTP_400_BAD_REQUEST)


        user = CustomUser(email=email)
        user.set_password(password)
        user.save()

        return Response({'msg': 'User successfully created'}, status=HTTP_200_OK)