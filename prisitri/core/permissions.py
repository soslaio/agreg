
from rest_framework import permissions


class IsObjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.criado_por == request.user


class IsObjectOwnerOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool((obj.criado_por == request.user) or request.user.is_staff)
