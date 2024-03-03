# Generated by Django 3.2 on 2024-02-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20240225_1457'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='onli_one_rewiew',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='onli_one_review'),
        ),
    ]