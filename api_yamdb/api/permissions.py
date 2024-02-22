from rest_framework import permissions
from users.models import Roles


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return
        return (
            request.user.role == Roles.ADMIN
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return
        return (
            request.user.role == Roles.ADMIN
            or request.user.is_superuser
        )
        
