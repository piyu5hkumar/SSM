from django import forms
from django.forms import widgets
from django.forms.widgets import PasswordInput


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label="New Password", min_length=8, widget=forms.PasswordInput
    )
    confirm_new_password = forms.CharField(
        label="Confirm New Password", min_length=8, widget=forms.PasswordInput
    )
