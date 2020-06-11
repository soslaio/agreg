
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import EmpresaViewSet, TipoRecursoViewSet, UsuarioViewSet


router = routers.DefaultRouter()
router.register('empresas', EmpresaViewSet)
router.register('tipos_recursos', TipoRecursoViewSet)

router.register('usuarios', UsuarioViewSet, basename='usuarios')

corepatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls)
]
