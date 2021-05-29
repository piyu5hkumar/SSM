# rest_framework imports
from rest_framework import serializers

# django imports
from django.conf import settings

# additional imports
from ..models import User, Otp


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=255)
    new_password = serializers.CharField(min_length=8, max_length=225)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8, max_length=255)


class ForgotPasswordSerializer(serializers.ModelSerializer):
    is_email = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['is_email', 'email', 'phone_number']
        extra_kwargs = {
            'phone_number': {
                'required': True,
                'allow_null': True,
                'validators': []
            },
            'email': {
                'required': True,
                'validators': []
            },
        }

    def validate(self, data):
        if data['is_email']:
            if not data['email']:
                raise serializers.ValidationError(
                    {'email': 'Please Enter an Email address'}
                )
        else:
            if not data['phone_number']:
                raise serializers.ValidationError(
                    {'phone_number': 'Please Enter a Phone number'}
                )
        return data


class ValidateOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=10, max_length=10)
    otp_received = serializers.CharField(min_length=settings.OTP_LENGTH, max_length=settings.OTP_LENGTH)
