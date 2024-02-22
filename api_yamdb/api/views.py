from django.contrib.auth import get_user_model
from rest_framework import (filters, generics, status,
                            viewsets, mixins)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.utils import send_confirmation_code
from django_filters import rest_framework as f
from reviews.models import Title, Category, Genre

from .permissions import AdminOnly, AdminOrReadOnly
from .serializers import (SignupSerializer, TokenObtainSerializer,
                          UserProfileSerializer, UserSerializer,
                          TitleSerializer, GenreSerializer,
                          CategorySerializer)

User = get_user_model()


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'), email=request.data.get('email')):
            user = User.objects.get(username=request.data['username'], email=request.data['email'])
            send_confirmation_code(user)
            return Response({'detail': 'user already exists, sent a new confirmation code'}, status=status.HTTP_200_OK)
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
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


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


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'



class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleFilter(f.FilterSet):
    genre = f.CharFilter(lookup_expr='slug')
    category = f.CharFilter(lookup_expr='slug')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = (f.DjangoFilterBackend,)
    filterset_class = TitleFilter
