from django.forms import Form, ModelForm, CharField, TextInput, EmailField, PasswordInput, EmailInput,NumberInput, Select,DateInput
from .models import User


class LoginForm(Form):
    email = EmailField(
        min_length=5,
        max_length=50,
        label='Email',
        required=True,
        widget=EmailInput({
            'class': 'form-control',
        })
    )

    password = CharField(
        min_length=4,
        max_length=25,
        label='Password',
        required=True,
        widget=PasswordInput({
            'class': 'form-control',
        })
    )

class RegistrationForm(ModelForm):
    
    confirm_password = CharField(
        min_length=8,
        max_length=50,
        label='Confirm Password',
        required=True,
        widget=PasswordInput({
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'date_of_birth',
            'gender',
            'password',
            
        ]
        widgets =  {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'phone_number': NumberInput(attrs={'class': 'form-control'}),
            'date_of_birth': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),

        }

class ProfileUpdateForm(RegistrationForm):
    password = None
    confirm_password = None