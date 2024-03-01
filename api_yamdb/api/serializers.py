from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
