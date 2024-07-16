from django import forms
from django.forms import Form,IntegerField
from .models import ParentsDetails, PartnerPreference,FriendRequest



class ParentsDetailsForm(forms.ModelForm):
    class Meta:
        model = ParentsDetails
        fields = [
            'father_name', 'father_occupation',
            'mother_name', 'mother_occupation', 
            'siblings_count',
            'annual_income',
            'permanent_address', 'present_address',
            'country', 'state', 'district', 
            'height', 'weight',
            'caste', 'religion',
            'zodiac_sign', 'horoscope',
        ]
        widgets = {
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'mother_occupation': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'siblings_count': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'annual_income': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'required': 'true','rows': 3}),
            'present_address': forms.Textarea(attrs={'class': 'form-control', 'required': 'true','rows': 3}),
            'country': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'state': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select', 'required': 'true'}),
            'district': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select', 'required': 'true'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'caste': forms.Select(attrs={'class': 'form-control', 'required': 'true', 'placeholder': 'Select'}),
            'religion': forms.Select(attrs={'class': 'form-control', 'required': 'true', 'placeholder': 'Select'}),
            'zodiac_sign': forms.Select(attrs={'class': 'form-control', 'required': 'true', 'placeholder': 'Select'}),
            'horoscope': forms.FileInput(attrs={'class': 'form-control', 'required': 'true'}),
        }

class PartnerPreferenceForm(forms.ModelForm):
    class Meta:
        model = PartnerPreference
        fields = [
            'age_min', 'age_max', 'caste', 'religion', 'height_min', 
            'height_max', 'weight_min', 'weight_max', 'income_min', 'income_max', 
            'qualification'
        ]
        widgets = {
            'age_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'caste': forms.Select(attrs={'class': 'form-control'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            'height_min': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'height_max': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'weight_min': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'weight_max': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'income_min': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'income_max': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'qualification': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
        }

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['to_user']

