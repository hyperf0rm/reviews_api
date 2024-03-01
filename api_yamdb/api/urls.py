from django.urls import include, path
from rest_framework import routers

from .views import SignupView, TokenObtainView, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')

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
