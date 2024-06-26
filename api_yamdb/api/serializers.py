import datetime as dt

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['view'].action == 'me':
            self.fields['role'].read_only = True


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):

        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Cannot use "me" as username.')

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'User with such username already exists.')
        return value

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'User with such email already exists.')
        return value


class TokenObtainSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    def validate(self, data):

        user = get_object_or_404(User, username=data.get('username'))

        if not User.objects.filter(
            username=data.get('username'),
            confirmation_code=data.get('confirmation_code')
        ).exists():
            raise serializers.ValidationError(
                'Wrong credentials, please check and try again.')

        refresh = self.get_token(user)
        data['token'] = str(refresh.access_token)

        return {'token': data['token']}


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

    def __init__(self, *args, **kwargs):
        super(TitleSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['genre'] = GenreSerializer(many=True)
            self.fields['category'] = CategorySerializer()

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
