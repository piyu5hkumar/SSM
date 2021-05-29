from django.contrib import admin
from .models import *

# Register your models here.

# @admin.register(User)
# class UserProfile(admin.ModelAdmin):
#     list_display = [field.name for field in User._meta.fields]

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display =  [field.name for field in UserProfile._meta.fields]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "phone_number",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
    ]


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "username",
        "first_name",
        "middle_name",
        "last_name",
        "d_o_b",
    ]


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "phone_number",
        "otp_sent",
        "otp_type",
        "date_created",
        "date_blocked",
        "attempts",
        "is_used",
        "is_latest"
    ]
