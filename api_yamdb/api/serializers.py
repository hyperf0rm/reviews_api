from rest_framework import serializers

from reviews.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для обработки запросов к объекту Категории."""
    class Meta:
        exclude = 'id',
        model = Category
