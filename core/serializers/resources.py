
from rest_framework import serializers
from rest_framework.reverse import reverse

from .summary import CompanySummarySerializer, ResourceTypeSummarySerializer, ExtendedUserSummarySerializer
from ..models import ScheduleType, Resource


class ResourceSummarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name_or_rt_name')

    class Meta:
        model = Resource
        fields = ('id', 'name', 'url')


class ResourceScheduleTypeSerializer(serializers.ModelSerializer):
    availability_url = serializers.SerializerMethodField()

    class Meta:
        model = ScheduleType
        fields = ('id', 'name', 'time', 'unit', 'url', 'availability_url')

    def get_availability_url(self, obj):
        resource_id = self.context['resource_id']
        availability_url = reverse('resources-availability', args=[resource_id, obj.id],
                                   request=self.context['request'])
        return availability_url


class ResourceSerializer(serializers.ModelSerializer):
    schedule_types = serializers.SerializerMethodField()
    company = CompanySummarySerializer()
    resource_type = ResourceTypeSummarySerializer()
    owner = ExtendedUserSummarySerializer()

    class Meta:
        model = Resource
        fields = '__all__'

    def get_schedule_types(self, obj):
        context = {
            'request': self.context['request'],
            'resource_id': obj.id
        }
        serializer = ResourceScheduleTypeSerializer(obj.schedule_types, many=True, context=context)
        return serializer.data
