
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Company, TipoRecurso, ExtendedUser, GrupoAprovacao


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class CompanySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'url')


class ExtendedUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = UserSerializer()
    companies = CompanySummarySerializer(many=True)

    class Meta:
        model = ExtendedUser
        fields = '__all__'


class ExtendedUserSummarySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = UserSerializer()

    class Meta:
        model = ExtendedUser
        fields = ('id', 'user', 'url')


class CompanySerializer(serializers.ModelSerializer):
    owner = ExtendedUserSummarySerializer()
    resource_types = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_resource_types(self, obj):
        types = obj.tiporecurso_set.all()
        request = self.context['request']
        serializer = ResourceTypeSummarySerializer(types, many=True, context={'request': request})
        return serializer.data


class GrupoAprovacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoAprovacao
        fields = '__all__'


class ApprovalGroupSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoAprovacao
        fields = ('id', 'nome', 'url')


class TipoRecursoSerializer(serializers.ModelSerializer):
    grupo = ApprovalGroupSummarySerializer()

    class Meta:
        model = TipoRecurso
        fields = '__all__'


class ResourceTypeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRecurso
        fields = ('id', 'name', 'url')






