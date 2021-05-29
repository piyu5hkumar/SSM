# django imports
from main_ssm.models.user_and_profile_model import UserProfile
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password

# rest_framework imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# additional imports
from ..models import User
from ..serializers import UserSerializer, LonginUserSerializer, UserProfileSerializer
from ..components import SSMResponse


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        resp = SSMResponse()
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        singed_up_user = serializer.save()
        resp.add_data_field(
            message=f'{singed_up_user.phone_number} has been successfully signed up'
        )
        resp.add_data_field(token=singed_up_user.get_token().key)

        return Response(resp.get_response(), status=status.HTTP_200_OK)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        resp = SSMResponse()
        serializer = LonginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # If a user is authenticated then logout that user
        if request.user.is_authenticated:
            resp.add_additional_info_field(logged_out_user=str(request.user))
            logout(request)

        phone_number = serializer.validated_data.get('phone_number', '')
        password = serializer.validated_data.get('password', '')

        try:
            user = User.objects.get(phone_number=phone_number)
            if check_password(password, user.password):
                login(request, user)
                user_token = Token.objects.get(user=user).key
                resp.add_data_field(message='User successfully logged in')
                resp.add_data_field(token=user_token)
            else:
                resp.add_error_field(message='Please enter correct Password')
        except User.DoesNotExist:
            resp.add_error_field(message='User doesn\'t exists')

        return Response(resp.get_response(), status=status.HTTP_200_OK)


class LogoutUser(APIView):
    def post(self, request):
        resp = SSMResponse()
        current_user = request.user
        resp.add_data_field(message=f'{current_user} is successfully Logged out')
        try:
            logout(request)
        except:
            resp.add_error_field(message=f'Unable to logout {current_user}')

        return Response(resp.get_response(), status=status.HTTP_200_OK)


class UserProfileInfo(APIView):
    def get(self, request):
        resp = SSMResponse()
        current_user = request.user
        serializer = UserProfileSerializer(current_user.user_profile)
        user_profile = serializer.data
        user_profile['phone_number'] = request.user.phone_number

        resp.add_data_field(message='UserProfile successfully fetched')
        resp.add_data_field(user_profile=user_profile)

        return Response(resp.get_response(), status=status.HTTP_200_OK)

    def post(self, request):
        resp = SSMResponse()
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        user_profile_details = serializer.data
        user_profile_details['phone_number'] = request.user.phone_number

        resp.add_data_field(message='Profile successfully updated')
        resp.add_data_field(user_profile=user_profile_details)
        return Response(resp.get_response(), status=status.HTTP_200_OK)
