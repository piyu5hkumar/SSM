from django import forms


class AccountForm(forms.Form):

    username = forms.CharField(
        min_length=4,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control  account-field-input',
                'id': 'username_field'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control account-field-input',
                'id': 'email_field'
            }
        )
    )


class PrivacyForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control privacy-field-input field-show',
                'id': 'old_password_field',
                'disabled': True
            }
        )
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control privacy-field-input field-show',
                'id': 'new_password_field',
                'disabled': True
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control privacy-field-input field-show',
                'id': 'confirm_password_field',
                'disabled': True
            }
        )
    )
