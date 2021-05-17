from django.contrib import admin
from .models import *

# Register your models here.

# @admin.register(User)
# class UserProfile(admin.ModelAdmin):
#     list_display = [field.name for field in User._meta.fields]

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display =  [field.name for field in UserProfile._meta.fields]


admin.site.register(User)
admin.site.register(UserProfile)