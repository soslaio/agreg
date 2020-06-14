
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import CompanyViewSet, ResourceTypeViewSet, ExtendedUserViewSet, ResourceViewSet, ScheduleTypeViewSet


router = routers.DefaultRouter()
router.register('companies', CompanyViewSet, basename='company')
router.register('resourcetypes', ResourceTypeViewSet)
router.register('resources', ResourceViewSet, basename='resource')
router.register('extendedusers', ExtendedUserViewSet, basename='extendeduser')
router.register('scheduletypes', ScheduleTypeViewSet, basename='scheduletype')

corepatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls)
]
