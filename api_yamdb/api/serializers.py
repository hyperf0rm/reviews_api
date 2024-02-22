from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Title, Genre, Category
import datetime as dt

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class SignupSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(
            max_length=254, 
            required=True,
            validators=[UniqueValidator(
                queryset=User.objects.all(),
                message='User with such email already exists.')])
        username = serializers.RegexField(
            regex=r'^[\w.@+-]+\Z',
            max_length=150,
            required=True,
            validators=[UniqueValidator(
                queryset=User.objects.all(),
                message='User with such username already exists.')])


        class Meta:
            model = User
            fields = ('username', 'email')

        def validate_username(self, value):
             
            if value.lower() == 'me':
                raise serializers.ValidationError('Cannot use "me" as username.')
            
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError('User with such username already exists.')
            return value
        
        def validate_email(self, value):
             
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError('User with such email already exists.')
            return value


class TokenObtainSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    def validate(self, data):

        user = get_object_or_404(User, username=data.get('username'))

        if not User.objects.filter(username=data.get('username'), confirmation_code=data.get('confirmation_code')).exists():
            raise serializers.ValidationError('Wrong credentials, please check and try again.')
        
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
    genre = serializers.SlugRelatedField(many=True, slug_field='slug', queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())


    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('id',)

    def __init__(self, *args, **kwargs):
        super(TitleSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
            self.fields['genre'] = GenreSerializer(many=True)
            self.fields['category'] = CategorySerializer()

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError('Enter a valid year.')
        return value

