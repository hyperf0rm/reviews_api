import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


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

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Год выпуска не может быть'
                                              'больше текущего.')
        return value


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки запросов к объекту Title. Только чтение."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
