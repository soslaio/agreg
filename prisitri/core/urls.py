
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import EmpresaViewSet, TipoRecursoViewSet, ExtendedUserViewSet


router = routers.DefaultRouter()
router.register('empresas', EmpresaViewSet, basename='empresa')
router.register('tipos_recursos', TipoRecursoViewSet)
router.register('usuarios', ExtendedUserViewSet, basename='extendeduser')

corepatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls)
]