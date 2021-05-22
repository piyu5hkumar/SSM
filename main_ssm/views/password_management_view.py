# rest_framework imports
from django import forms
from django.core.checks import messages
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# django imports
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views import View
from django.views.generic.edit import FormView
from django.shortcuts import HttpResponse, render
from django.conf import settings

# additional imports
from ..components import CustomResponse
from ..serializers import (
    PasswordSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
)
from ..models import User
from ..forms import ResetPasswordForm
import jwt
import time
import datetime


class CheckPassword(APIView):
    def post(self, request):
        resp = CustomResponse()
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password", "")
        if check_password(password, request.user.password):
            resp.add_data_field(message="Password matched successfully")
        else:
            resp.add_error_field(message="Old Password didn't match")
        return Response(resp.get_response(), status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def post(self, request):
        resp = CustomResponse()
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get("old_password", "")
        if check_password(old_password, request.user.password):
            new_password = serializer.validated_data.get("new_password", "")
            request.user.password = new_password
            request.user.save(update_fields=["password"])
            resp.add_data_field(message="Password successfully reset")
        else:
            resp.add_error_field(message="Please enter correct current password")
        return Response(resp.get_response(), status=status.HTTP_200_OK)


class ForgotPasswordTokenGenerator(PasswordResetTokenGenerator):
    """
    We will call make_token of PasswordRestTokenGenerator,
    which uses _make_token_with_timestamp(self, user, timestamp, legacy=False),
    which further uses __make_hash_value(self, user, timestamp)
    So we are overriding __make_hash_value(self, user, timestamp)
    it is using the user.password salt and user.last_login timestamp.

    Both will change, and the link will no longer be valid.
    Also the self.secret(SECRET_KEY) is used in the salted_hmac function(inside _make_token_with_timestamp(self, user, timestamp, legacy=False)).
    So unless your SECRET_KEY was compromised, it would be impossible to reproduce the hash value.

    """

    def _make_hash_value(self, user, timestamp):
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        return f"{user.pk}{user.password}{timestamp}{user.email}"


class ForgotPassword(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        resp = CustomResponse()

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_email = serializer.validated_data.get("is_email", True)

        if is_email:
            email = serializer.validated_data.get("email", "")
            base_url = "http://127.0.0.1:8000/api/reset_password"
            user_qs = User.objects.filter(email=email)

            if user_qs.exists():
                user = user_qs.first()
                user_uid = str(user.uid)
                reset_token_generator_object = ForgotPasswordTokenGenerator()
                password_reset_token = reset_token_generator_object.make_token(user)

                payload = {
                    "uid": user_uid,
                    "password_reset_token": password_reset_token,
                    "timestamp": time.time(),
                }
                jwt_token = jwt.encode(payload, "piyush")
                forgot_password_url = f"{base_url}/{jwt_token}"
                resp.add_data_field(message="Forgot password link send")
                resp.add_data_field(url=forgot_password_url)
            else:
                resp.add_error_field(message="User doesn't exists")
        else:
            pass
            phone_number = serializer.validated_data.get("phone_number", "")
            user_qs = User.objects.filter(phone_number=phone_number)

            if user_qs.exists():
                user = user_qs.first()
                user_uid = user.uid
            else:
                resp.add_error_field(message="User doesn't exists")

        return Response(resp.get_response(), status=status.HTTP_200_OK)


class ForgotPasswordPage(View):
    form = ResetPasswordForm()

    def is_token_valid(self, jwt_token):
        try:
            # This will also raise an exception on unsuccessful decode
            decoded_token = jwt.decode(jwt_token, "piyush", algorithms=["HS256"])

            # checking expiration of the jwt_token
            timestamp = decoded_token["timestamp"]
            timestamp_difference = time.time() - float(timestamp)

            timestamp_delta_limit = datetime.timedelta(
                hours=settings.JWT_TOKEN_EXPIRE_HOURS
            )
            timestamp_delta = datetime.timedelta(seconds=timestamp_difference)
            if timestamp_delta > timestamp_delta_limit:
                raise Exception(f"Token expired")

            # checking user exists with the provided uid or not
            # get automatically raises an exception when nothing is found
            uid = decoded_token["uid"]
            user = User.objects.get(uid=uid)

            # checking password_reset_token
            password_reset_token = decoded_token["password_reset_token"]
            reset_token_generator_object = ForgotPasswordTokenGenerator()
            if not reset_token_generator_object.check_token(user, password_reset_token):
                raise Exception("Invalid token")
        except Exception:
            return False, None, None

        return True, user, password_reset_token

    def get(self, request, jwt_token=None):
        valid, _, _ = self.is_token_valid(jwt_token)
        if not valid:
            return render(request, "main_ssm/invalid_page.html")

        return render(request, "main_ssm/reset_password.html", {"form": self.form})

    def post(self, request, jwt_token=None):
        valid, user, password_reset_token = self.is_token_valid(jwt_token)
        if not valid:
            return render(request, "main_ssm/invalid_page.html")

        new_password = request.POST.get("new_password", "")
        confirm_new_password = request.POST.get("confirm_new_password", "")

        if new_password != confirm_new_password:
            return render(request, "main_ssm/reset_password.html", {"form": self.form})

        user.password = new_password
        user.save(update_fields=["password"])
        return render(request, "main_ssm/reset_password_successful.html")
