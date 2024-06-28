from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

class User(AbstractUser):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        verbose_name='Phone number'
    )

    date_of_birth = models.DateField(
        null=True, 
        blank=True, 
        verbose_name='Date of birth'
    )

    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        blank=False, 
        verbose_name='Gender',
        default='M'
    )
    

@property
def is_basic_profile_complete(self):
    return all([
        self.first_name,
        self.last_name,
        self.email,
        self.password,
        self.username,
        self.phone_number,
        self.date_of_birth,
        self.gender
    ])

@property
def age(self):
    if self.date_of_birth is not None:
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)
    else:
        return None
