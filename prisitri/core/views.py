
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
# from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from .viewsets import PermissionedViewset
from .models import Company, TipoRecurso, ExtendedUser
from .permissions import IsObjectOwnerOrAdminUser, IsRelatedToCompanyOrAdminUser
from .serializer import (CompanySerializer, CompanySummarySerializer, ResourceTypeSummarySerializer,
                         ExtendedUserSerializer, ExtendedUserSummarySerializer)


class CompanyViewSet(PermissionedViewset):
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'retrieve': [IsRelatedToCompanyOrAdminUser]
    }

    def list(self, request):
        queryset = Company.objects.all()
        serializer = CompanySummarySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        empresas = Company.objects.all()
        empresa = get_object_or_404(empresas, pk=pk)
        self.check_object_permissions(self.request, empresa)
        serializer = CompanySerializer(empresa, context={'request': request})
        return Response(serializer.data)


class TipoRecursoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoRecurso.objects.all()
    serializer_class = ResourceTypeSummarySerializer
    permission_classes = [IsAdminUser]


class ExtendedUserViewSet(PermissionedViewset):
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'retrieve': [IsObjectOwnerOrAdminUser]
    }

    def list(self, request):
        queryset = ExtendedUser.objects.all()
        serializer = ExtendedUserSummarySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ExtendedUser.objects.all()
        usuario = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, usuario)
        serializer = ExtendedUserSerializer(usuario, context={'request': request})
        return Response(serializer.data)




