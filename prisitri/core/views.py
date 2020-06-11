
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .viewsets import PermissionedViewset
from .models import Empresa, TipoRecurso, Usuario
from .permissions import IsObjectOwnerOrAdminUser
from .serializer import EmpresaSerializer, TipoRecursoSerializer, UsuarioSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class TipoRecursoViewSet(viewsets.ModelViewSet):
    queryset = TipoRecurso.objects.all()
    serializer_class = TipoRecursoSerializer


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



