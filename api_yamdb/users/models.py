from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from users.constants import (CODE_LENGTH, EMAIL_MAX_LENGTH, NAME_MAX_LENGTH,
                             ROLE_LENGTH, STR_LIMIT)
from users.roles import Roles
from users.validators import validate_username


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be set.')
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Roles.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Model for User objects."""

    username = models.CharField(
        'username',
        max_length=NAME_MAX_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Enter a valid username',
                code='invalid_username'
            ),
            validate_username])
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
    first_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=ROLE_LENGTH,
        choices=[(choice.value, choice.value) for choice in Roles],
        default=Roles.USER)
    confirmation_code = models.CharField(max_length=CODE_LENGTH,
                                         null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_users')
        ]

    @property
    def is_admin(self):
        """Returns True if user is admin, False otherwise."""
        return (self.is_staff
                or self.is_superuser
                or self.role == Roles.ADMIN)

    @property
    def is_moderator(self):
        """Returns True if user is moderator, False otherwise."""
        return self.role == Roles.MODERATOR

    def __str__(self):
        return self.username[:STR_LIMIT]
