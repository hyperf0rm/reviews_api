# Generated by Django 3.2 on 2024-02-22 18:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(code='invalid_category_slug', message='Enter a valid category slug', regex='^[-a-zA-Z0-9_]+$')])),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(code='invalid_genre_slug', message='Enter a valid genre slug', regex='^[-a-zA-Z0-9_]+$')])),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('year', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.category')),
                ('genres', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.genre')),
            ],
        ),
    ]
