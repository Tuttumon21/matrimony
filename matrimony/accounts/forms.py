from django.forms import Form, ModelForm, CharField, TextInput, EmailField, PasswordInput, EmailInput,NumberInput, Select,DateInput,FileInput
from .models import User
from django import forms


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
            'username',
            'email',
            'password',
            
        ]
        widgets =  {
            
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),

        }

class ProfileUpdateForm(RegistrationForm):
    password = None
    confirm_password = None

class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'gender',
            'age',
            'phone_number',
            'date_of_birth',
            'education_level',
            'profile_pic',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'placeholder': 'Age will Automatically calculate'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }