# Generated by Django 4.2.13 on 2024-07-09 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrimonyApp', '0004_alter_parentsdetails_caste_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parentsdetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents_details', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='partnerpreference',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_preference', to='matrimonyApp.parentsdetails'),
        ),
    ]