from django import forms
from django.forms import Form,IntegerField
from .models import ParentsDetails, PartnerPreference
from .widgets import RangeSliderWidget


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
            'zodiac_sign': forms.TextInput(attrs={'class': 'form-control'}),
            'horoscope': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PartnerPreferenceForm(forms.ModelForm):
    age_range = forms.CharField(widget=RangeSliderWidget(attrs={'min': '18', 'max': '60'}), label='Age Range')
    class Meta:
        model = PartnerPreference
        fields = [
            # 'age_min', 'age_max', 'caste', 'religion', 
            'age_range',
            'height_min', 'height_max', 'weight_min', 'weight_max', 
            'income_min', 'income_max', 'qualification','caste',
            'religion',
        ]
        widgets = {
            # 'age_min': forms.NumberInput(attrs={'type': 'range', 'min': '18', 'max': '70', 'step': '1', 'class': 'form-range'}),
            # 'age_max': forms.NumberInput(attrs={'type': 'range', 'min': '18', 'max': '70', 'step': '1', 'class': 'form-range'}),
            'height_min': forms.NumberInput(attrs={'type': 'range', 'min': '100', 'max': '250', 'step': '1', 'class': 'form-range'}),
            'height_max': forms.NumberInput(attrs={'type': 'range', 'min': '100', 'max': '250', 'step': '1', 'class': 'form-range'}),
            'weight_min': forms.NumberInput(attrs={'type': 'range', 'min': '30', 'max': '200', 'step': '1', 'class': 'form-range'}),
            'weight_max': forms.NumberInput(attrs={'type': 'range', 'min': '30', 'max': '200', 'step': '1', 'class': 'form-range'}),
            'income_min': forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '1000000', 'step': '1000', 'class': 'form-range'}),
            'income_max': forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '1000000', 'step': '1000', 'class': 'form-range'}),
            'caste': forms.Select(attrs={'class': 'form-control'}),

            'religion': forms.Select(attrs={'class': 'form-control'}),
            'qualification': forms.Select(attrs={'class': 'form-control'}),
        }

