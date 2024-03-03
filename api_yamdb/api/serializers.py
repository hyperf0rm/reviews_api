from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for processing requests to User objects."""

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
    """Serializer for signing up and obtaining confirmation code."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        """Validate username and return valid value."""
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Cannot use "me" as username.')
        return value


class TokenObtainSerializer(TokenObtainPairSerializer):
    """Serializer for obtaining access token."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    def validate(self, data):
        """Validate request data and return access token."""
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
    """Serializer for processing requests to Category objects."""

    class Meta:
        model = Category
        exclude = 'id',


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for processing requests to Genre objects."""

    class Meta:
        model = Genre
        exclude = 'id',


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for processing requests to Title objects."""

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

    def get_rating(self, obj):
        """Get average rating of the Title object."""
        reviews = Review.objects.filter(title=obj.id)
        if not reviews:
            return None
        average_rating = reviews.aggregate(Avg('score'))['score__avg']
        return int(average_rating)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for processing requests to Review objects."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
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


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for processing requests to Comment objects."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        exclude = ('review',)
