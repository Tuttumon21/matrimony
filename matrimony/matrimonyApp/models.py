from django.db import models
# from django.contrib.auth.models import User
from accounts.models import User
# Create your models here.

class ParentsDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parents_details')
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)
    siblings_count = models.PositiveIntegerField()
    annual_income = models.PositiveIntegerField()
    permanent_address = models.TextField()
    present_address = models.TextField()
    country = models.CharField(
        max_length=10, 
        blank=False,
        verbose_name='country',
        default='NONE',
        choices=[('INDIA', 'India')]
    )
    state = models.CharField(
        max_length=10,
        blank=False,
        verbose_name='state',
        default='NONE',
        choices=[('KERALA','Kerala'),('TAMILNADU','Tamilnadu')]
    )
    district = models.CharField(
        max_length=25,
        blank=False,
        verbose_name='district',
        default='NONE',
        choices=[('ALAPPUZHA', 'Alappuzha'),('ERNAKULAM', 'Ernakulam'),('IDUKKI', 'Idukki'),('KASARAGOD', 'Kasaragod'),
        ('KOZHIKODE', 'Kozhikode'),('KOLLAM', 'Kollam'),('KOTTAYAM', 'Kottayam'),('MALAPPURAM', 'Malappuram'),('PALAKKAD', 'Palakkad'),
        ('PATHANAMTHITTA', 'Pathanamthitta'),('THIRUVANANTHAPURAM', 'Thiruvananthapuram'),('THRISSUR', 'Thrissur'),('WAYANAD', 'Wayanad')])
    
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()

    caste = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    zodiac_sign = models.CharField(max_length=100)
    horoscope = models.FileField(upload_to='horoscopes/')

class PartnerPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner_preference')
    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField()
    caste = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    height_min = models.PositiveIntegerField()
    height_max = models.PositiveIntegerField()
    weight_min = models.PositiveIntegerField()
    weight_max = models.PositiveIntegerField()
    income_min = models.PositiveIntegerField()
    income_max = models.PositiveIntegerField()
    qualification = models.CharField(
        max_length=50,
        choices=[
            ('SSLC', 'SSLC'),
            ('PLUSTWO', 'Plus Two'),
            ('BACHELOR', 'Bachelors'),
            ('MASTERS', 'Masters'),
            ('PHD', 'PhD'),
        ]
    )