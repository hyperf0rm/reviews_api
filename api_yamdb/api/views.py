from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from api.mixins import CreateListDeleteViewSet
from api.permissions import CreateDeleteOnlyAdmin
from api.serializers import CategorySerializer
from reviews.models import Category


class CategoryViewSet(CreateListDeleteViewSet):
    """Вьюсет для создания, получения списка
    и удаления обьектов класса Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [CreateDeleteOnlyAdmin,]
    lookup_field = 'slug'
