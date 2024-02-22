from django.contrib.auth import get_user_model
from rest_framework import (filters, generics, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.utils import send_confirmation_code

from .permissions import AdminOnly
from .serializers import (SignupSerializer, TokenObtainSerializer,
                          UserProfileSerializer, UserSerializer)

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
