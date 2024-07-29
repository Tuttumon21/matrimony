# Generated by Django 4.2.13 on 2024-07-28 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrimonyApp', '0017_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_id', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('currency', models.CharField(blank=True, max_length=10, null=True)),
                ('payment_status', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('receipt_url', models.URLField(blank=True, null=True)),
                ('payment_method_type', models.CharField(blank=True, max_length=50, null=True)),
                ('hosted_invoice_url', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='inactive', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]