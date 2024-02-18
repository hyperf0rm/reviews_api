from django.db import models

from reviews.constants import MAX_TITLE_LEN, STR_LIMIT


class Category(models.Model):
    """Модель для объектов Категории."""
    name = models.CharField('Заголовок', max_length=MAX_TITLE_LEN)
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
