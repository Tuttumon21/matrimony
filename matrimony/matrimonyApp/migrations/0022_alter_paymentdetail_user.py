# Generated by Django 4.2.13 on 2024-07-31 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrimonyApp', '0021_savedprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_detail', to=settings.AUTH_USER_MODEL),
        ),
    ]