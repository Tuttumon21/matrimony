from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# import datetime
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name='email address',
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
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        blank=False, 
        verbose_name='Gender',
    )
    education_level = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Education level',
        choices=[('SSLC', 'SSLC'), ('PLUSTWO', 'PLUSTWO'), ('BACHELOR', 'BACHELOR'), ('MASTERS', 'MASTERS'), ('PHD', 'PHD')]
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)

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

# @property
# def age(self):
#     if self.date_of_birth is not None:
#         return int((datetime.date.today() - self.date_of_birth).days / 365.25)
#     else:
#         return None
