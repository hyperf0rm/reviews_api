from django.db import models

from reviews.constants import MAX_TITLE_LEN, STR_LIMIT


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
        null=True,
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
