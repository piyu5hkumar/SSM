from django.db.models import fields
from rest_framework import serializers
from ..models import User


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=255)
    new_password = serializers.CharField(min_length=8, max_length=225)
