from django import forms
from django.forms import Form,IntegerField
from .models import ParentsDetails, PartnerPreference



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
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'siblings_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'annual_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            'present_address': forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control', 'label': 'Select'}),
            'district': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'caste': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
            'zodiac_sign': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select'}),
            'horoscope': forms.FileInput(attrs={'class': 'form-control'}),
        }

# class PartnerPreferenceForm(forms.ModelForm):
