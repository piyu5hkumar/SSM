from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
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


    def __str__(self):
        return self.phone_number


class UserProfile(models.Model):
    ssmuser = models.OneToOneField(
        User,
        related_name="ssm_user_profile",
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
