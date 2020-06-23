
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from ..models import Company, ResourceType, ExtendedUser, ApprovalGroup, ScheduleType, Resource, Order, Schedule


class UserSummarySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'url')

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_url(self, obj):
        request = self.context['request']
        return reverse('user-detail', args=[obj.username], request=request)


class ExtendedUserSummarySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = UserSummarySerializer()

    class Meta:
        model = ExtendedUser
        fields = ('id', 'user', 'url')


class OrderSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'resource', 'requester')


class CompanySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'url')


class ResourceTypeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ('id', 'name', 'url')


class ScheduleTypeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleType
        fields = ('id', 'name', 'time', 'unit', 'url')


class ScheduleSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'start', 'end')


class ApprovalGroupSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalGroup
        fields = ('id', 'name', 'url')
