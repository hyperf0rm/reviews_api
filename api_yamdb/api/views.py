from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from api.filters import TitleFilter
from api.mixins import CreateListDeleteViewSet
from api.permissions import CreateDeleteOnlyAdmin, IsAuthorOrModeratorOrAdmin
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleListSerializer, TitleSerializer)
from reviews.models import Category, Comment, Genre, Review, Title


class CategoryViewSet(CreateListDeleteViewSet):
    """Вьюсет для создания, получения списка
    и удаления обьектов класса Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [CreateDeleteOnlyAdmin, ]
    lookup_field = 'slug'


class GenreViewSet(CreateListDeleteViewSet):
    """Вьюсет для создания, получения списка
    и удаления обьектов класса Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [CreateDeleteOnlyAdmin, ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для класса Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [CreateDeleteOnlyAdmin,]
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthorOrModeratorOrAdmin, ]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=False)
        serializer.save(title=self.get_title(), author=self.request.user)

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """API для комментариев к отзывам."""
    pagination_class = PageNumberPagination
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthorOrModeratorOrAdmin, ]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=False)
        serializer.save(review=self.get_review(), author=self.request.user)

    def get_queryset(self):
        return self.get_review().comments.all()
