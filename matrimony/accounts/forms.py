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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()

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

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

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
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'placeholder': 'Age will Automatically calculate'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'true'}),
            'education_level': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control', 'required': 'true'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

class LifeStyleForm(forms.ModelForm):
    
    hobbies = forms.MultipleChoiceField(
        choices=User.HOBBIES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    interest = forms.MultipleChoiceField(
        choices=User.INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = [
            'smoking_status',
            'drinking_status',
            'hobbies',
            'interest',
        ]
        widgets = {
            'smoking_status': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'drinking_status': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'hobbies': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'required': 'true'}),
            'interest': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'required': 'true'}),
        }
    def clean_hobbies(self):
        return ','.join(self.cleaned_data.get('hobbies', []))

    def clean_interest(self):
        return ','.join(self.cleaned_data.get('interest', []))

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            if kwargs['instance'].hobbies:
                initial['hobbies'] = kwargs['instance'].hobbies.split(',')
            if kwargs['instance'].interest:
                initial['interest'] = kwargs['instance'].interest.split(',')
        super(LifeStyleForm, self).__init__(*args, **kwargs)



class EmploymentStatusForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'employment_status',
            'company_name',
            'designation',
            'work_location',
            'job_title',
            'expert_level',
        ]
        widgets = {
            'employment_status': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'work_location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'expert_level': forms.Select(attrs={'class': 'form-control'}),
        }

class RelationshipTypeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['relationship_type']
        widgets = {
            'relationship_type': forms.Select(attrs={'class':'form-control', 'required': 'true'}),
        }