from django import forms
from main_ssm.models import User


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        min_length=10,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                # 'id': 'inlineFormInputGroupUsername',
                # 'placeholder': "Phone Number"
            }
        )
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password_field',
                # 'placeholder': "Password"
            }
        )
    )
