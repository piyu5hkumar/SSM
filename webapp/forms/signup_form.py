from django import forms


class SignUpForm(forms.Form):
    phone_number = forms.CharField(
        min_length=10,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password_field',
            }
        )
    )
    re_password = forms.CharField(
        min_length=8,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
