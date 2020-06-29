
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import ExtendedUser


class IsObjectOwnerOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool((obj.user == request.user) or request.user.is_staff)


class IsRelatedToCompanyOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        users = ExtendedUser.objects.all()
        db_user = get_object_or_404(users, user=request.user)
        companies = db_user.companies.all()
        companies_ids = set(companies.values_list('id', flat=True))
        return bool((obj.id in companies_ids) or request.user.is_staff)
