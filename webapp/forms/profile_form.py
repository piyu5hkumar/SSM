from django import forms


class ProfileForm(forms.Form):

    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control  field-input',
                'id': 'first_name_field'
            }
        )
    )

    middle_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control  field-input',
                'id': 'middle_name_field'
            }
        ),
        required=False,
    )

    last_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control  field-input',
                'id': 'last_name_field'
            }
        )
    )

    d_o_b = forms.DateTimeField(
        label='Date Of Birth',
        widget=forms.DateTimeInput(
            format='%d-%m-%Y',
            attrs={
                'type': 'date',
                'class': 'form-control  field-input',
                'id': 'dob_field'
            }
        ),
        required=False
    )
