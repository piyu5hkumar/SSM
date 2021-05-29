# rest_framework imports
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

# django imports
from django.contrib.auth.hashers import check_password
from django.views import View
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import login, logout

# additional imports
from ..components import (
    SSMResponse,
    SendGrid,
    ForgotPasswordTokenGenerator,
    Twilio
)
from ..serializers import (
    PasswordSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    ValidateOtpSerializer
)
from ..models import User, Otp
from ..forms import ResetPasswordForm
import jwt
import time
import datetime
import os


JWT_SIGNATURE = os.environ.get('JWT_SIGNATURE', '')


class CheckPassword(APIView):
    def post(self, request):
        resp = SSMResponse()
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password', '')
        if check_password(password, request.user.password):
            resp.add_data_field(message='Password matched successfully')
        else:
            resp.add_error_field(message='Old Password didn\'t match')
        return Response(resp.get_response(), status=status.HTTP_200_OK)


class ChangePassword(APIView):
    def post(self, request):
        resp = SSMResponse()
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get('old_password', '')
        if check_password(old_password, request.user.password):
            new_password = serializer.validated_data.get('new_password', '')
            request.user.password = new_password
            request.user.save(update_fields=['password'])
            resp.add_data_field(message='Password successfully reset')
        else:
            resp.add_error_field(message='Please enter correct current password')
        return Response(resp.get_response(), status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def post(self, request):
        resp = SSMResponse()
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.password = serializer.validated_data.get('new_password', '')
        request.user.save(update_fields=['password'])
        resp.add_data_field(message='Password reset successful, please login to continue')
        logout(request)
        return Response(resp.get_response(), status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        resp = SSMResponse()

        serializer = ForgotPasswordSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        is_email = serializer.validated_data.get('is_email', True)

        try:
            if is_email:
                email = serializer.validated_data.get('email', '')
                base_url = 'http://127.0.0.1:8000/api/reset_password'

                user = User.objects.get(email=email)  # Raises User.DoesNotExist on unsuccess
                user_uid = str(user.uid)

                reset_token_generator_object = ForgotPasswordTokenGenerator()
                password_reset_token = reset_token_generator_object.make_token(user)

                payload = {
                    'uid': user_uid,
                    'password_reset_token': password_reset_token,
                    'timestamp': time.time(),
                }
                jwt_token = jwt.encode(payload, JWT_SIGNATURE)
                forgot_password_url = f'{base_url}/{jwt_token}'

                sendgrid_obj = SendGrid()
                is_success, sendgrid_response = sendgrid_obj.send_email(
                    to_email=email, verification_link=forgot_password_url
                )

                if is_success:
                    resp.add_data_field(
                        message='Forgot password link successfully sent'
                    )
                    resp.add_additional_info_field(sendgrid_response=sendgrid_response)
                else:
                    resp.add_error_field(message='Unable to send message')
                    resp.add_additional_info_field(sendgrid_response=sendgrid_response)

            else:
                phone_number = serializer.validated_data.get(
                    'phone_number', ''
                )  # Raises User.DoesNotExist on unsuccess

                User.objects.get(phone_number=phone_number)
                twilio_object = Twilio()
                resp.add_additional_info_field(twilio_use=twilio_object.TWILIO_USE)

                is_success, message = twilio_object.send_otp(
                    phone_number=phone_number,
                    otp_type=Otp.OtpTypes.FORGOT_PASSWORD,
                    length=settings.OTP_LENGTH
                )

                if is_success:
                    resp.add_data_field(message=message)
                else:
                    resp.add_error_field(message=message)

        except User.DoesNotExist:
            resp.add_error_field(message='User dosn\'t exists')
        return Response(resp.get_response(), status=status.HTTP_200_OK)

    def post(self, request):
        resp = SSMResponse()

        serializer = ValidateOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            Otp.objects.get(
                otp_sent=serializer.validated_data['otp_received'],
                otp_type=Otp.OtpTypes.FORGOT_PASSWORD
            )
            user = User.objects.get(phone_number=serializer.validated_data['phone_number'])

            is_validated, message = Otp.validate_otp(
                phone_number=serializer.validated_data['phone_number'],
                otp_received=serializer.validated_data['otp_received'],
                otp_type=Otp.OtpTypes.FORGOT_PASSWORD
            )
            if is_validated:
                login(request, user)
                user_token = Token.objects.get(user=user).key
                resp.add_data_field(message=message)
                resp.add_data_field(token=user_token)

            else:
                resp.add_error_field(message=message)
        except Otp.DoesNotExist as e:
            resp.add_error_field(message='Invalid OTP')
        except User.DoesNotExist as e:
            resp.add_error_field(message='User with this Phone Number doesn\'t exist')
        finally:
            return Response(resp.get_response(), status=status.HTTP_200_OK)


class ForgotPasswordPage(View):
    form = ResetPasswordForm()

    def is_token_valid(self, jwt_token):

        try:
            # This will also raise an exception on unsuccessful decode
            decoded_token = jwt.decode(jwt_token, JWT_SIGNATURE, algorithms=['HS256'])

            # checking expiration of the jwt_token
            timestamp = decoded_token['timestamp']
            timestamp_difference = time.time() - float(timestamp)

            timestamp_delta_limit = datetime.timedelta(
                hours=settings.JWT_TOKEN_EXPIRE_HOURS
            )
            timestamp_delta = datetime.timedelta(seconds=timestamp_difference)
            if timestamp_delta > timestamp_delta_limit:
                raise Exception(f'Token expired')

            # checking user exists with the provided uid or not
            # get automatically raises an exception when nothing is found
            uid = decoded_token['uid']
            user = User.objects.get(uid=uid)

            # checking password_reset_token
            password_reset_token = decoded_token['password_reset_token']
            reset_token_generator_object = ForgotPasswordTokenGenerator()
            if not reset_token_generator_object.check_token(user, password_reset_token):
                raise Exception('Invalid token')
        except Exception:
            return False, None, None

        return True, user, password_reset_token

    def get(self, request, jwt_token=None):
        valid, _, _ = self.is_token_valid(jwt_token)
        if not valid:
            return render(request, 'main_ssm/invalid_page.html')

        return render(request, 'main_ssm/reset_password.html', {'form': self.form})

    def post(self, request, jwt_token=None):
        valid, user, password_reset_token = self.is_token_valid(jwt_token)
        if not valid:
            return render(request, 'main_ssm/invalid_page.html')

        new_password = request.POST.get('new_password', '')
        confirm_new_password = request.POST.get('confirm_new_password', '')

        if new_password != confirm_new_password:
            return render(
                request,
                'main_ssm/reset_password.html',
                context={
                    'form': self.form,
                    'error': 'Please enter same password in the both fields',
                },
            )

        user.password = new_password
        user.save(update_fields=['password'])
        return render(request, 'main_ssm/reset_password_successful.html')
