# Generated by Django 3.2 on 2024-03-03 11:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Заголовок')),
                ('slug', models.SlugField(help_text='Разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Заголовок')),
                ('slug', models.SlugField(unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('year', models.IntegerField(verbose_name='Год выпуска')),
                ('description', models.TextField(verbose_name='Описание')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(blank=True, related_name='titles', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('name',),
                'default_related_name': 'titles',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('score', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], verbose_name='Оценка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-pub_date',),
                'default_related_name': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.title')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария к отзыву')),
                ('review', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'комментарий к отзыву',
                'verbose_name_plural': 'Комментарии к отзывам',
                'ordering': ('-pub_date',),
                'default_related_name': 'comments',
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_reviews'),
        ),
    ]
