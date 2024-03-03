from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.filters import TitleFilter
from api.mixins import CreateListDeleteViewSet
from api.permissions import (AdminOnly, IsAdminModeratorOrAuthor,
                             IsAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer, TitleSerializer,
                             TokenObtainSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title
from users.utils import send_confirmation_code

User = get_user_model()


class SignupView(generics.CreateAPIView):
    """
    Viewset for signing up and obtaining confirmation code.

    post: takes username and email and sends confirmation code to email.
    """

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ):
            user = User.objects.get(
                username=request.data['username'],
                email=request.data['email']
            )
            send_confirmation_code(user)
            return Response({
                'detail': 'User already exists, sent a new confirmation code.'
            },
                status=status.HTTP_200_OK)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# doesnt work
'''    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email']
        )
        send_confirmation_code(user)
        if not created:
            return Response({
                'detail': 'User already exists, sent a new confirmation code.'
            },
                status=status.HTTP_200_OK)
        if created:
            return Response(serializer.data, status=status.HTTP_200_OK)'''


class TokenObtainView(TokenObtainPairView):
    """
    Viewset for obtaining access token.

    post: takes username and confirmation code and returns access token
    """

    serializer_class = TokenObtainSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AdminOnly]
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        if request.method == 'PATCH':
            return self.partial_update(request)


class CategoryViewSet(CreateListDeleteViewSet):
    """
    Viewset for handling requests to Category objects.

    get: returns a list of all categories.

    post: creates a category.

    delete: deletes a category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDeleteViewSet):
    """
    Viewset for handling requests to Genre objects.

    get: returns a list of all genres.

    post: creates a genre.

    delete: deletes a genre.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling requests to Title objects.

    get: returns a list of all title or a specific title.

    post: creates a title.

    patch: updates a title.

    delete: deletes a title.
    """

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ('name', 'year', 'category', 'genre')
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling requests to Review objects.

    get: returns a list of all reviews for a title or a specific review.

    post: creates a review.

    patch: updates a review.

    delete: deletes a review.
    """

    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')
    permission_classes = [IsAdminModeratorOrAuthor]

    def get_queryset(self):
        return self.get_title().reviews.all()

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data.update({'title': self.get_title().id})
        request.POST._mutable = False
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling requests to Comment objects.

    get: returns a list of all comments for a review or a specific comment.

    post: creates a comment.

    patch: updates a comment.

    delete: deletes a comment.
    """

    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')
    permission_classes = [IsAdminModeratorOrAuthor]

    def get_review(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return get_object_or_404(Review,
                                 pk=self.kwargs.get('review_id'),
                                 title=title)

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)

    def get_queryset(self):
        return self.get_review().comments.all()
