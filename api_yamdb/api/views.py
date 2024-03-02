from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.utils import send_confirmation_code
from reviews.models import Category, Genre, Review, Title
from api.filters import TitleFilter
from api.mixins import CreateListDeleteViewSet

from .permissions import (AdminOnly, CreateDeleteOnlyAdmin,
                          IsAuthorOrModeratorOrAdmin)
from .serializers import (SignupSerializer, TokenObtainSerializer,
                          UserProfileSerializer, UserSerializer,
                          CategorySerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializer)

User = get_user_model()


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            user = User.objects.get(
                username=request.data['username'],
                email=request.data['email']
            )
            send_confirmation_code(user)
            return Response({
                'detail': 'User already exists, sent a new confirmation code'
            },
                status=status.HTTP_200_OK)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AdminOnly,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,),
            serializer_class=UserProfileSerializer)
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        if request.method == 'PATCH':
            return self.partial_update(request)


class CategoryViewSet(CreateListDeleteViewSet):
    """Вьюсет для создания, получения списка
    и удаления обьектов класса Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (CreateDeleteOnlyAdmin,)
    lookup_field = 'slug'


class GenreViewSet(CreateListDeleteViewSet):
    """Вьюсет для создания, получения списка
    и удаления обьектов класса Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (CreateDeleteOnlyAdmin,)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для класса Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (CreateDeleteOnlyAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset for Review model"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')
    permission_classes = (IsAuthorOrModeratorOrAdmin,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=False)
        serializer.save(title=self.get_title(), author=self.request.user)

    def get_queryset(self):
        return self.get_title().reviews.all()
