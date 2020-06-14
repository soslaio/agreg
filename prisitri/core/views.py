
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
# from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from .viewsets import PermissionedViewset
from .models import Empresa, TipoRecurso, ExtendedUser
from .permissions import IsObjectOwnerOrAdminUser, IsRelatedToCompanyOrAdminUser
from .serializer import (CompanySerializer, CompanySummarySerializer, ResourceTypeSummarySerializer,
                         ExtendedUserSerializer, ExtendedUserSummarySerializer)


class EmpresaViewSet(PermissionedViewset):
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'retrieve': [IsRelatedToCompanyOrAdminUser]
    }

    def list(self, request):
        queryset = Empresa.objects.all()
        serializer = CompanySummarySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        empresas = Empresa.objects.all()
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
        serializer = ExtendedUserSerializer(usuario)
        return Response(serializer.data)




