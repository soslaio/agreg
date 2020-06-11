
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import Usuario


class IsObjectOwnerOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool((obj.criado_por == request.user) or request.user.is_staff)


class IsRelatedToCompanyOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        users = Usuario.objects.all()
        db_user = get_object_or_404(users, user=request.user)
        companies = db_user.empresas.all()
        companies_ids = set(companies.values_list('id', flat=True))
        return bool((obj.id in companies_ids) or request.user.is_staff)
