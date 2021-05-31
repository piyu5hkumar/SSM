from django import forms


class UserProfileForm(forms.Form):
    username = forms.CharField(
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    middle_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    last_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    d_o_b = forms.DateTimeField(
        label='Date Of Birth',
        widget=forms.DateTimeInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )
