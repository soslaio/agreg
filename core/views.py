
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, action

from .viewsets import PermissionedViewset
from .models import Company, ResourceType, ExtendedUser, Resource, ScheduleType, ApprovalGroup, Order
from .permissions import IsObjectOwnerOrAdminUser, IsRelatedToCompanyOrAdminUser
from .serializers import (CompanySerializer, CompanySummarySerializer, ResourceTypeSummarySerializer, SlotSerializer,
                          ExtendedUserSummarySerializer, ResourceSerializer, ResourceSummarySerializer, OrderSerializer,
                          ScheduleTypeSummarySerializer, ScheduleTypeSerializer, UserFullSerializer,
                          ResourceTypeSerializer, ApprovalGroupSummarySerializer, ScheduleSummarySerializer,
                          OrderSummarySerializer, UserSummarySerializer, ExtendedUserFullSerializer)


class ApprovalGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApprovalGroup.objects.all()
    serializer_class = ApprovalGroupSummarySerializer


class OrderViewSet(PermissionedViewset):
    def list(self, request):
        queryset = Order.objects.prefetch_related('requester').all()
        serializer = OrderSummarySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        orders = Order.objects.all()
        order = get_object_or_404(orders, pk=pk)
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


class CompanyViewSet(PermissionedViewset):
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'retrieve': [IsRelatedToCompanyOrAdminUser]
    }

    def list(self, request):
        queryset = Company.objects.all()
        serializer = CompanySummarySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        empresas = Company.objects.all()
        empresa = get_object_or_404(empresas, pk=pk)
        self.check_object_permissions(self.request, empresa)
        serializer = CompanySerializer(empresa, context={'request': request})
        return Response(serializer.data)


class ResourceTypeViewSet(PermissionedViewset):
    def list(self, request):
        resource_types = ResourceType.objects.all()
        serializer = ResourceTypeSummarySerializer(resource_types, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        resource_types = ResourceType.objects.all()
        resource_type = get_object_or_404(resource_types, pk=pk)
        serializer = ResourceTypeSerializer(resource_type, context={'request': request})
        return Response(serializer.data)


class ScheduleTypeViewSet(PermissionedViewset):
    queryset = ScheduleType.objects.all()
    serializer_class = ScheduleTypeSummarySerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        queryset = ScheduleType.objects.all()
        serializer = ScheduleTypeSummarySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        scheduletypes = ScheduleType.objects.all()
        scheduletype = get_object_or_404(scheduletypes, pk=pk)
        serializer = ScheduleTypeSerializer(scheduletype, context={'request': request})
        return Response(serializer.data)


class ResourceViewSet(PermissionedViewset):
    permission_classes_by_action = {
        'list': [IsAdminUser]
    }

    def list(self, request):
        queryset = Resource.objects.prefetch_related('resource_type', 'company', 'schedule_types').all()
        serializer = ResourceSummarySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        resources = Resource.objects.all()
        resource = get_object_or_404(resources, pk=pk)
        serializer = ResourceSerializer(resource, context={'request': request})
        return Response(serializer.data)

    @api_view(['GET'])
    def availability(request, pk=None, schedule_type_id=None):
        resources = Resource.objects.all()
        resource = get_object_or_404(resources, pk=pk)

        schedule_types = ScheduleType.objects.all()
        schedule_type = get_object_or_404(schedule_types, pk=schedule_type_id)

        date = request.query_params.get('date', datetime.strftime(timezone.now(), '%Y-%m-%d'))
        availabilities = resource.get_availability(schedule_type, date)
        serializer = SlotSerializer(availabilities, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def schedules(self, request, pk=None):
        resources = Resource.objects.all()
        resource = get_object_or_404(resources, pk=pk)
        date = request.query_params.get('date', datetime.strftime(timezone.now(), '%Y-%m-%d'))
        schedules = resource.get_schedules(date)
        serializer = ScheduleSummarySerializer(schedules, many=True, context={'request': request})
        return Response(serializer.data)


class UserViewSet(PermissionedViewset):
    permission_classes_by_action = {
        'list': [IsAdminUser]
    }

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSummarySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=pk)
        # self.check_object_permissions(self.request, usuario)
        serializer = UserFullSerializer(user, context={'request': request})
        return Response(serializer.data)


class ExtendedUserViewSet(PermissionedViewset):
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'retrieve': [IsObjectOwnerOrAdminUser]
    }

    def list(self, request):
        queryset = ExtendedUser.objects.all()
        serializer = ExtendedUserSummarySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ExtendedUser.objects.all()
        usuario = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, usuario)
        serializer = ExtendedUserFullSerializer(usuario, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def orders(self, request, pk=None):
        orders = Order.objects.filter(requester__id=pk)
        serializer = OrderSummarySerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

