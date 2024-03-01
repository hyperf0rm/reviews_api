# Generated by Django 3.2 on 2024-02-21 21:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Enter a valid username', regex='^[\\w.@+-]+\\Z')], verbose_name='Username'),
        ),
    ]