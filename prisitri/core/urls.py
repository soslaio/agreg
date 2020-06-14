
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import (CompanyViewSet, ResourceTypeViewSet, ExtendedUserViewSet, ResourceViewSet, ScheduleTypeViewSet,
                    ApprovalGroupViewSet)


router = routers.DefaultRouter()
router.register('companies', CompanyViewSet, basename='company')
router.register('resourcetypes', ResourceTypeViewSet, basename='resourcetype')
router.register('resources', ResourceViewSet, basename='resource')
router.register('extendedusers', ExtendedUserViewSet, basename='extendeduser')
router.register('scheduletypes', ScheduleTypeViewSet, basename='scheduletype')
router.register('approvalgroups', ApprovalGroupViewSet, basename='approvalgroup')

corepatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls)
]
