# django imports
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db import transaction

# rest_framework imports
from rest_framework.authtoken.models import Token

# additional imports
from datetime import time
from ..manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        primary_key=True, validators=[MinLengthValidator(10)], max_length=10
    )
    password = models.CharField(
        null=False, blank=False, validators=[MinLengthValidator(8)], max_length=225
    )
    date_joined = models.DateTimeField(null=False, blank=False, default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_token(self):
        return Token.objects.get(user=self)

    def __str__(self):
        return self.phone_number


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="user_profile",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    username = models.CharField(
        unique=True,
        null=False,
        blank=True,
        validators=[MinLengthValidator(4)],
        max_length=30,
        default="",
    )

    # null and blank are False by default

    first_name = models.CharField(blank=True, max_length=20, default="")
    middle_name = models.CharField(blank=True, max_length=20, default="")
    last_name = models.CharField(blank=True, max_length=20, default="")
    d_o_b = models.DateField(null=True, blank=True, default=None)

    def __str__(self):
        name = self.username
        name = self.ssmuser.phone_number if name == "" else name
        return name


################################################## signals ##################################################


@receiver(pre_save, sender=User)
def hash_password(sender, instance, *args, **kwargs):
    # password will be only hashed in two condition
    # 1. is_staff and is_superuser are false, because if it is then the create_superuser->create_user is already handling it.
    # 2. if we are updating some fields, because we don't want to update the password again.

    if (not instance.is_staff and not instance.is_superuser) or (
        "password" in kwargs["update_fields"]
    ):
        instance.set_password(instance.password)


@receiver(post_save, sender=User)
def create_token(sender, instance, created, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)


@transaction.atomic
@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    user_to_login = kwargs.get("user")
    Token.objects.filter(user=user_to_login).delete()
    Token.objects.create(user=user_to_login)

    # it will automatically calls kwargs.get("user").save(update_fields=["last_login"])


@transaction.atomic
@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    user_to_logout = kwargs.get("user")
    user_to_logout.last_logout = timezone.now()
    user_to_logout.save(update_fields=["last_logout"])
    Token.objects.filter(user=user_to_logout).delete()


@receiver(pre_save, sender=UserProfile)
def capitalize_first_letter(sender, instance, *args, **kwargs):
    instance.username = instance.username.lower()
    instance.first_name = instance.first_name.title()
    instance.middle_name = instance.middle_name.title()
    instance.last_name = instance.last_name.title()
