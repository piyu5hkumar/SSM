# rest_framework imports
from rest_framework import serializers

# additional imports
from ..models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password", "phone_number"]


class LonginUserSerializer(serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        extra_kwargs = {"phone_number": {"validators": []}}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ["user"]

    def create(self, *args, **kwargs):
        arg_dict = args[0]

        user = arg_dict["user"]
        user_profile, created = UserProfile.objects.update_or_create(
            user=user, defaults=arg_dict
        )

        return user_profile
