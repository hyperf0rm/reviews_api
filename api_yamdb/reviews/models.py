from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import MAX_TITLE_LENGTH, STR_LIMIT
from reviews.validators import validate_year

User = get_user_model()


class BaseNameModel(models.Model):
    """Abstract base class for model inheritance (name)."""

    name = models.CharField('Заголовок', max_length=MAX_TITLE_LENGTH)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:STR_LIMIT]


class BaseSlugModel(models.Model):
    """Abstract base class for model inheritance (slug)."""

    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        abstract = True


class Category(BaseNameModel, BaseSlugModel):
    """Model for Category objects."""

    class Meta(BaseNameModel.Meta):
        default_related_name = 'categories'
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(BaseNameModel, BaseSlugModel):
    """Model for Genre objects."""

    class Meta(BaseNameModel.Meta):
        default_related_name = 'genres'
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(BaseNameModel):
    """Model for Title objects."""

    year = models.SmallIntegerField('Год выпуска', validators=[validate_year])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta(BaseNameModel.Meta):
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'


class BaseReviewCommentModel(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(BaseReviewCommentModel):
    """Model for Review objects."""

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
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField('Оценка', choices=SCORE_CHOICES)

    class Meta(BaseReviewCommentModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_reviews'
            )
        ]

    def __str__(self):
        return (f'Текст отзыва на {self.title.name[:STR_LIMIT]}'
                f'от {self.author.username[:STR_LIMIT]}:'
                f'{self.text[:STR_LIMIT]}')


class Comment(BaseReviewCommentModel):
    """Model for Comment objects."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(BaseReviewCommentModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзывам'

    def __str__(self):
        return (f'Текст комментария от {self.author[:STR_LIMIT]}'
                f'на отзыв от {self.review.author[:STR_LIMIT]}:'
                f'{self.text[:STR_LIMIT]}')


class GenreTitle(models.Model):
    """Intermediate model for ManyToMany relations between Title and Genre."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
