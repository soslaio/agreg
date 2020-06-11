
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
# from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from .viewsets import PermissionedViewset
from .models import Empresa, TipoRecurso, Usuario
from .permissions import IsObjectOwnerOrAdminUser, IsRelatedToCompanyOrAdminUser
from .serializer import EmpresaSerializer, TipoRecursoSerializer, UsuarioSerializer


class EmpresaViewSet(PermissionedViewset):
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'retrieve': [IsRelatedToCompanyOrAdminUser]
    }

    def list(self, request):
        queryset = Empresa.objects.all()
        serializer = EmpresaSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        empresas = Empresa.objects.all()
        empresa = get_object_or_404(empresas, pk=pk)
        self.check_object_permissions(self.request, empresa)
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)


class TipoRecursoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoRecurso.objects.all()
    serializer_class = TipoRecursoSerializer
    permission_classes = [IsAdminUser]


class UsuarioViewSet(PermissionedViewset):
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'retrieve': [IsObjectOwnerOrAdminUser]
    }

    def list(self, request):
        queryset = Usuario.objects.all()
        serializer = UsuarioSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Usuario.objects.all()
        usuario = get_object_or_404(queryset, user__username=pk)
        self.check_object_permissions(self.request, usuario)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)




