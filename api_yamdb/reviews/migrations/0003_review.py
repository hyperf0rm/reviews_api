# Generated by Django 3.2 on 2024-02-21 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20240221_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('score', models.IntegerField(verbose_name='Оценка')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.title', verbose_name='Отзыв')),
            ],
        ),
    ]
