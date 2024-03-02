from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Title, Genre, Category, Review
import datetime as dt

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role')


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ('role',)


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):

        if value.lower() == 'me':
            raise serializers.ValidationError('Cannot use "me" as username.')

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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.ReadOnlyField()

    class Meta:
        model = Title
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TitleSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['genre'] = GenreSerializer(many=True)
            self.fields['category'] = CategorySerializer()

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                'The year cannot be greater than the current one.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'title': {'write_only': True},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]
