# Generated by Django 3.2.1 on 2021-05-28 05:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_ssm', '0008_alter_otp_otp_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp_sent',
            field=models.CharField(max_length=6, validators=[django.core.validators.MinLengthValidator(6)]),
        ),
    ]
