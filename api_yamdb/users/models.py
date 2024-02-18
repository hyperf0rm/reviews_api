from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField('Biography', blank=True)
    role = models.TextField('Роль', blank=True)
    # поле role - заглушка для тестов, реализация должна быть другой
