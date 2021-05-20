from django.db.models import fields
from ..models import User
from rest_framework import serializers
from django.core.validators import MinLengthValidator, MaxLengthValidator


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "password"]
        extra_kwargs = {
            "phone_number": {
                "validators": []
            }
        }
