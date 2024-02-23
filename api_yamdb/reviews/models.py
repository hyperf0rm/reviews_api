from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import MAX_TITLE_LEN, STR_LIMIT

User = get_user_model()


class Category(models.Model):
    """Модель для объектов Категории."""
    name = models.CharField('Название', max_length=MAX_TITLE_LEN)
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:STR_LIMIT]


class Genre(models.Model):
    """Модель для объектов Жанров."""
    name = models.CharField('Заголовок', max_length=256)
    slug = models.SlugField(
        'Идентификатор',
        unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:STR_LIMIT]


class Title(models.Model):
    """Модель для объектов Произведений."""
    name = models.CharField('Название', max_length=MAX_TITLE_LEN)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'titles'
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:STR_LIMIT]


class Review(models.Model):
    SCORE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    # score = models.IntegerField('Оценка')
    score = models.IntegerField(verbose_name='Оценка', choices=SCORE_CHOICES)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )

    class Meta:
        default_related_name = 'rewiews'
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = '-pub_date',
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='onli_one_rewiew'
            )
        ]


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
