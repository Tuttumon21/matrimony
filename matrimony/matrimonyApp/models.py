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

    caste = models.CharField(max_length=100,choices=[ ('Brahmin', 'Brahmin'), ('Kshatriya', 'Kshatriya'), ('Vaishya', 'Vaishya'),
    ('Shudra', 'Shudra'), ('Dalit', 'Dalit'), ('Koli', 'Koli'), ('Gujar', 'Gujar'),
    ('Lodhi', 'Lodhi'), (' Yadav', 'Yadav'), ('Jat', 'Jat') ,('Others','Others')]
)
    religion = models.CharField(max_length=100,choices=[ ('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Hinduism', 'Hinduism'),
    ('Buddhism', 'Buddhism'), ('Sikhism', 'Sikhism'), ('Judaism', 'Judaism'), ('Baha’i', 'Baha’i'), ('Jainism', 'Jainism'),
    ('Shintoism', 'Shintoism'), ('Cao Dai', 'Cao Dai'),('Others','Others')])
    zodiac_sign = models.CharField(max_length=100,choices=[ ('Aries', 'Aries'), ('Taurus', 'Taurus'), ('Gemini', 'Gemini'), ('Cancer', 'Cancer'),
    ('Leo', 'Leo'), ('Virgo', 'Virgo'), ('Libra', 'Libra'),('Scorpio', 'Scorpio'),('Sagittarius', 'Sagittarius'),('Capricorn','Capricorn'),
    ('Aquarius', 'Aquarius'),('Pisces', 'Pisces')])
    horoscope = models.FileField(upload_to='horoscopes/')
    interested_gender = models.CharField(max_length=6, choices=[('MALE', 'Male'),('FEMALE', 'Female'),('BOTH', 'Both')], default='BOTH')

class PartnerPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner_preference')
    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField()
    caste = models.CharField(max_length=100,choices=[ ('Brahmin', 'Brahmin'), ('Kshatriya', 'Kshatriya'), ('Vaishya', 'Vaishya'),
    ('Shudra', 'Shudra'), ('Dalit', 'Dalit'), ('Koli', 'Koli'), ('Gujar', 'Gujar'),
    ('Lodhi', 'Lodhi'), (' Yadav', 'Yadav'), ('Jat', 'Jat') ,('Others','Others')]
)
    religion = models.CharField(max_length=100,choices=[ ('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Hinduism', 'Hinduism'),
    ('Buddhism', 'Buddhism'), ('Sikhism', 'Sikhism'), ('Judaism', 'Judaism'), ('Baha’i', 'Baha’i'), ('Jainism', 'Jainism'),
    ('Shintoism', 'Shintoism'), ('Cao Dai', 'Cao Dai'),('Others','Others')])
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

class FriendRequest(models.Model):
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}: {self.status}"
    
    def unfriend(self):
        if self.status == 'accepted':
            self.delete()

class ProfileExclusion(models.Model):
    user = models.ForeignKey(User, related_name='exclusions', on_delete=models.CASCADE)
    excluded_profile = models.ForeignKey(User, related_name='excluded_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'excluded_profile')

    def __str__(self):
        return f"{self.user} excluded {self.excluded_profile}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.body[:50]}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)
    plan_id = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank initially
    plan_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.plan_id} ({self.plan_type})'

class PaymentDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_mode = models.CharField(max_length=255, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    customer_id = models.CharField(max_length=255, null=True, blank=True)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    payment_status = models.CharField(max_length=50, null=True, blank=True)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    receipt_url = models.CharField(max_length=255, null=True, blank=True)
    payment_method_type = models.CharField(max_length=50, null=True, blank=True)
    hosted_invoice_url = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    subscription_id = models.CharField(max_length=255, null=True, blank=True)
    invoice_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='inactive')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'PaymentDetail for {self.user.username} - {self.session_id}'