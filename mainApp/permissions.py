from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsOwnerObj(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.parser_context['kwargs']['users_username'] == request.user.username

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
