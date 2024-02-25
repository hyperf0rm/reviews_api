import datetime as dt

from django.db.models import Avg
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для обработки запросов к объекту Category"""

    class Meta:
        exclude = 'id',
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки запросов к объекту Genre."""

    class Meta:
        exclude = 'id',
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатр для обработки запросов к объекту Title"""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Год выпуска не может быть'
                                              'больше текущего.')
        return value

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        if not reviews:
            return None
        average_rating = reviews.aggregate(Avg('score'))['score__avg']
        return int(average_rating)


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки запросов к объекту Title. Только чтение."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        if not reviews:
            return None
        average_rating = reviews.aggregate(Avg('score'))['score__avg']
        return int(average_rating)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError('К одному произведению можно'
                                  'оставить только один отзыв.', code=404)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        exclude = ('review',)
