from rest_framework import permissions


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
