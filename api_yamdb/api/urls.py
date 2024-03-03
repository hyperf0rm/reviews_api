from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignupView, TitleViewSet,
                       TokenObtainView, UserViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('users',
                   UserViewSet,
                   basename='user')
router_v1.register('categories',
                   CategoryViewSet,
                   basename='category')
router_v1.register('genres',
                   GenreViewSet,
                   basename='genre')
router_v1.register('titles',
                   TitleViewSet,
                   basename='title')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')

auth = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain'),
]

v1 = [
    path('', include(router_v1.urls)),
    path('', include(auth))
]

urlpatterns = [
    path('v1/', include(v1)),
]
