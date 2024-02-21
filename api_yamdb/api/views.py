from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from api.filters import TitleFilter
from api.mixins import CreateListDeleteViewSet
from api.permissions import CreateDeleteOnlyAdmin
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleListSerializer, TitleSerializer)
from reviews.models import Category, Genre, Title


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
