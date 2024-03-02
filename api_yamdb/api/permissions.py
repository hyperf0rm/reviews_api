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


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == Roles.ADMIN
                or request.user.is_superuser
                or request.method in permissions.SAFE_METHODS
            )
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role == Roles.ADMIN
                or request.user.is_superuser
                or request.method in permissions.SAFE_METHODS
            )
        return request.method in permissions.SAFE_METHODS


class IsAdminModeratorOrAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == Roles.ADMIN
            or request.user.role == Roles.MODERATOR
            or obj.author == request.user
            or request.user.is_superuser
        )
