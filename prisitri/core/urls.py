
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import CompanyViewSet, TipoRecursoViewSet, ExtendedUserViewSet


router = routers.DefaultRouter()
router.register('companies', CompanyViewSet, basename='company')
router.register('tipos_recursos', TipoRecursoViewSet)
router.register('extendedusers', ExtendedUserViewSet, basename='extendeduser')

corepatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls)
]
