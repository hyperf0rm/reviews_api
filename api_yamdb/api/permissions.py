from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Grants permission only to admins."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Grants permission to any user if request method is safe.

    If request method is not safe, grants permission only to admins.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)


class IsAdminModeratorOrAuthor(permissions.IsAuthenticatedOrReadOnly):
    """
    Grants permission to any user if request method is safe.

    If request method is not safe, grants permission only to admins,
    moderators or authors of objects.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
