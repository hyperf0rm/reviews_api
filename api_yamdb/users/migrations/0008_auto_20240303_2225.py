# Generated by Django 3.2 on 2024-03-03 19:25

import django.core.validators
from django.db import migrations, models
import users.roles
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20240302_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default=users.roles.Roles['USER'], max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Enter a valid username', regex='^[\\w.@+-]+\\Z'), users.validators.validate_username], verbose_name='username'),
        ),
    ]
