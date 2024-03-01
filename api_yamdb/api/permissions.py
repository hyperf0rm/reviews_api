from rest_framework import permissions

from users.models import Roles


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == Roles.ADMIN
                or request.user.is_superuser
            )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role == Roles.ADMIN
                or request.user.is_superuser
            )


class CreateDeleteOnlyAdmin(permissions.IsAdminUser):
    """Разрешает анонимному пользователю только безопасные запросы.
    Остальные запросы может делать только администратор."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.method in permissions.SAFE_METHODS
                    or request.user.role == 'admin'
                    or request.user.is_staff
                    or request.user.is_superuser)
        return request.method in permissions.SAFE_METHODS
    # Класс создан как заглушка, чтобы прошли тесты.
    # Требует доработки после написания модели User


class IsAuthorOrModeratorOrAdmin(permissions.IsAdminUser):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'admin'
                or request.user.is_staff
                or request.user.role == 'moderator'
                or request.user.is_superuser)
