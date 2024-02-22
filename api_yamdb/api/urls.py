from django.urls import include, path
from rest_framework import routers

from .views import SignupView, TokenObtainView, UserViewSet, TitleViewSet, GenreViewSet, CategoryViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('categories', CategoryViewSet, basename='category')

authpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(authpatterns)),
]
