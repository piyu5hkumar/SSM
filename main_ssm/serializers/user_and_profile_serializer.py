from django.db.models import fields
from ..models import User, UserProfile
from rest_framework import serializers
from django.core.validators import MinLengthValidator, MaxLengthValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password", "phone_number"]


class LonginUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields
        extra_kwargs = {"phone_number": {"validators": []}}


