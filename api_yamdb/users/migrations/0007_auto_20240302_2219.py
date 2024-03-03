# Generated by Django 3.2 on 2024-03-02 19:19

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_merge_0002_user_role_0005_auto_20240222_0137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username',)},
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default=users.models.Roles['USER'], max_length=10, verbose_name='role'),
        ),
    ]