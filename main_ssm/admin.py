from django.contrib import admin
from .models import *

# Register your models here.


class SsmUserAdmin(admin.ModelAdmin):
    list_display = [
        "phone_number",
        "date_joined",
        "last_login",
        "last_logout",
    ]


admin.site.register(User, SsmUserAdmin)


@admin.register(UserProfile)
class SSmUserProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "middle_name", "last_name", "d_o_b"]
