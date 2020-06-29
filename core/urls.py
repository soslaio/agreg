
from django.urls import path, include
from rest_framework import routers
from .views import (CompanyViewSet, ResourceTypeViewSet, ExtendedUserViewSet, ResourceViewSet, ScheduleTypeViewSet,
                    ApprovalGroupViewSet, OrderViewSet, UserViewSet)


router = routers.DefaultRouter()
router.register('companies', CompanyViewSet, basename='company')
router.register('resourcetypes', ResourceTypeViewSet, basename='resourcetype')
router.register('resources', ResourceViewSet, basename='resource')
router.register('extendedusers', ExtendedUserViewSet, basename='extendeduser')
router.register('users', UserViewSet, basename='user')
router.register('scheduletypes', ScheduleTypeViewSet, basename='scheduletype')
router.register('approvalgroups', ApprovalGroupViewSet, basename='approvalgroup')
router.register('orders', OrderViewSet, basename='order')

corepatterns = [
    path('', include(router.urls)),
    path('resources/<str:pk>/availabilities/<str:schedule_type_id>/',
         ResourceViewSet.availability, name='resources-availability')
]
