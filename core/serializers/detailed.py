
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from ..models import (Company, ResourceType, ExtendedUser, ApprovalGroup, ScheduleType, Order, Schedule, CompanyType,
                      Unit)
from .summary import (CompanySummarySerializer, ExtendedUserSummarySerializer, ResourceTypeSummarySerializer,
                      ApprovalGroupSummarySerializer, ScheduleSummarySerializer, CompanyTypeSummarySerializer,
                      UnitSummarySerializer)
from .resources import ResourceSummarySerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class ExtendedUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    companies = CompanySummarySerializer(many=True)

    class Meta:
        model = ExtendedUser
        fields = '__all__'


class ExtendedUserFullSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = UserSerializer()
    companies = CompanySummarySerializer(many=True)

    class Meta:
        model = ExtendedUser
        fields = '__all__'


class UserFullSerializer(serializers.ModelSerializer):
    extended_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password',)

    def get_extended_user(self, obj):
        request = self.context['request']
        all_extended_user = ExtendedUser.objects.all()
        extended_user = get_object_or_404(all_extended_user, user=obj.id)
        serializer = ExtendedUserSerializer(extended_user, context={'request': request})
        return serializer.data


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


class CompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    owner = ExtendedUserSummarySerializer()
    resource_types = ResourceTypeSummarySerializer(many=True)
    company_type = CompanyTypeSummarySerializer()
    units = UnitSummarySerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'


class ApprovalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalGroup
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    resources = ResourceSummarySerializer(many=True)
    owner = ExtendedUserSummarySerializer()
    company = CompanySummarySerializer()

    class Meta:
        model = Unit
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
    schedules = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_schedules(self, obj):
        serializer = ScheduleSummarySerializer(instance=obj.schedules, many=True)
        return serializer.data

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
