
from rest_framework import serializers
from ..models import Company, ResourceType, ExtendedUser, ApprovalGroup, Resource, ScheduleType
from .summary import (CompanySummarySerializer, ExtendedUserSummarySerializer, ResourceTypeSummarySerializer,
                      ScheduleTypeSummarySerializer, ApprovalGroupSummarySerializer, UserSerializer)


class ExtendedUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = UserSerializer()
    companies = CompanySummarySerializer(many=True)

    class Meta:
        model = ExtendedUser
        fields = '__all__'


class ScheduleTypeSerializer(serializers.ModelSerializer):
    owner = ExtendedUserSummarySerializer()
    tipo_recurso = ResourceTypeSummarySerializer()

    class Meta:
        model = ScheduleType
        fields = '__all__'


class ResourceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'url')


class ResourceSerializer(serializers.ModelSerializer):
    tipos_alocacao = ScheduleTypeSummarySerializer(many=True)

    class Meta:
        model = Resource
        fields = '__all__'


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


