
from django.urls import path, include
from rest_framework import routers
from .views import EmpresaViewSet


router = routers.DefaultRouter()
router.register(r'empresas', EmpresaViewSet)

corepatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
