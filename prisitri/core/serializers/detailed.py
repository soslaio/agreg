
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Company, ResourceType, ExtendedUser, ApprovalGroup, ScheduleType, Order, Schedule
from .summary import (CompanySummarySerializer, ExtendedUserSummarySerializer, ResourceTypeSummarySerializer,
                      ApprovalGroupSummarySerializer)
from .resources import ResourceSummarySerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class ExtendedUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = UserSerializer()
    companies = CompanySummarySerializer(many=True)

    class Meta:
        model = ExtendedUser
        fields = '__all__'


class ScheduleTypeSerializer(serializers.ModelSerializer):
    owner = ExtendedUserSummarySerializer()
    resource_type = ResourceTypeSummarySerializer()

    class Meta:
        model = ScheduleType
        fields = '__all__'


class ResourceTypeSerializer(serializers.ModelSerializer):
    owner = ExtendedUserSummarySerializer()
    company = CompanySummarySerializer()
    approval_group = ApprovalGroupSummarySerializer()
    resources = serializers.SerializerMethodField()

    class Meta:
        model = ResourceType
        fields = '__all__'

    def get_resources(self, obj):
        resources = obj.resource_set.all()
        request = self.context['request']
        serializer = ResourceSummarySerializer(resources, many=True, context={'request': request})
        return serializer.data


class CompanySerializer(serializers.ModelSerializer):
    owner = ExtendedUserSummarySerializer()
    resource_types = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_resource_types(self, obj):
        types = obj.resourcetype_set.all()
        request = self.context['request']
        serializer = ResourceTypeSummarySerializer(types, many=True, context={'request': request})
        return serializer.data


class ApprovalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalGroup
        fields = '__all__'


class TipoRecursoSerializer(serializers.ModelSerializer):
    grupo = ApprovalGroupSummarySerializer()

    class Meta:
        model = ResourceType
        fields = '__all__'


class SlotSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)

        # create schedules related to order
        schedules_data = self.initial_data.pop('schedules')
        for schedule in schedules_data:
            schedule['order'] = order.id
            serializer = ScheduleSerializer(data=schedule)
            serializer.is_valid()
            serializer.save()

        return order
