
from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Company, ResourceType, ExtendedUser, ApprovalGroup, ScheduleType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class CompanySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'url')


class ExtendedUserSummarySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = UserSerializer()

    class Meta:
        model = ExtendedUser
        fields = ('id', 'user', 'url')


class ResourceTypeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ('id', 'name', 'url')


class ScheduleTypeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleType
        fields = ('id', 'name', 'tempo', 'unidade', 'url')


class ApprovalGroupSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalGroup
        fields = ('id', 'nome', 'url')
