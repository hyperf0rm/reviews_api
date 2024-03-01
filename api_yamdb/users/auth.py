from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()

class AuthenticationWithoutPassword(BaseBackend):

    def authenticate(self, request, username=None):
        if username is None:
            username = request.data.get('username', '')
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None