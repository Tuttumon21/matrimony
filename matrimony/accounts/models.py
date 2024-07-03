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
        unique=True, 
        blank=True,
        null=True,
        verbose_name='Phone number'
    )
    date_of_birth = models.DateField(
        null=True, 
        blank=True, 
        verbose_name='Date of birth'
    )
    gender = models.CharField(
        max_length=10, 
        blank=False, 
        verbose_name='Gender',
        choices=[('MALE', 'Male'),('FEMALE', 'Female'),('OTHER', 'Other')] 
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

    smoking_status = models.CharField(max_length=20,default='Non-smoker', choices=[('Non-smoker', 'Non-smoker'),('Smoker', 'Smoker'),('Occasional', 'Occasional'),])
    drinking_status = models.CharField(max_length=20,default='Non-drinker', choices=[('Non-drinker', 'Non-drinker'),('Drinker', 'Drinker'),('Occasional', 'Occasional'),])

    HOBBIES_CHOICES = [
        ('reading', 'Reading'),
        ('travelling', 'Travelling'),
        ('sports', 'Sports'),
        ('music', 'Music'),
    ]

    INTEREST_CHOICES = [
        ('technology', 'Technology'),
        ('art', 'Art'),
        ('fitness', 'Fitness'),
        ('cooking', 'Cooking'),
    ]

    hobbies = models.TextField(blank=True)
    interest = models.TextField(blank=True)


    employment_status = models.CharField(max_length=10,default='employee', choices=[('employee', 'Employee'),('employer', 'Employer'),('jobseeker', 'Job Seeker'),])
    company_name = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    work_location = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    expert_level = models.CharField(max_length=15, blank=True,default='beginner', choices=[('beginner', 'Beginner'),('intermediate', 'Intermediate'),('expert', 'Expert'),])










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
