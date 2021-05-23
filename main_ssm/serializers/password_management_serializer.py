# rest_framework imports
from django.db.models import fields
from rest_framework import serializers

# additional imports
from ..models import User
from main_ssm import models


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=255)
    new_password = serializers.CharField(min_length=8, max_length=225)


class ForgotPasswordSerializer(serializers.ModelSerializer):
    is_email = serializers.BooleanField()

    class Meta:
        model = User
        fields = ["is_email", "email", "phone_number"]
        extra_kwargs = {
            "phone_number": {"required": True, "allow_null": True, "validators": []},
            "email": {"required": True, "validators": []},
        }

    def validate(self, data):
        if data["is_email"]:
            if not data["email"]:
                raise serializers.ValidationError(
                    {"email": "Please Enter an Email address"}
                )
                # ("not a valid email you shit!!!")
        else:
            if not data["phone_number"]:
                raise serializers.ValidationError(
                    {"phone_number": "Please Enter a Phone number"}
                )
        return data
