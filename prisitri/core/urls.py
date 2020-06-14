
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import CompanyViewSet, ResourceTypeViewSet, ExtendedUserViewSet


router = routers.DefaultRouter()
router.register('companies', CompanyViewSet, basename='company')
router.register('resourcetypes', ResourceTypeViewSet)
router.register('extendedusers', ExtendedUserViewSet, basename='extendeduser')

corepatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls)
]
