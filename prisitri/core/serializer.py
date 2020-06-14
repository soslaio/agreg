
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Empresa, TipoRecurso, ExtendedUser, GrupoAprovacao


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class ExtendedUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = UserSerializer()
    # empresas = CompanySummarySerializer(many=True)

    class Meta:
        model = ExtendedUser
        fields = '__all__'


class ExtendedUserSummarySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = UserSerializer()

    class Meta:
        model = ExtendedUser
        fields = ('id', 'user', 'url')


class CompanySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('id', 'name', 'url')


class CompanySerializer(serializers.ModelSerializer):
    # owner = ExtendedUserSummarySerializer(default=None)
    resource_types = serializers.SerializerMethodField()

    class Meta:
        model = Empresa
        fields = '__all__'

    def get_resource_types(self, obj):
        types = obj.tiporecurso_set.all()
        serializer = ResourceTypeSummarySerializer(types, many=True)
        return serializer.data


class GrupoAprovacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoAprovacao
        fields = '__all__'


class ApprovalGroupSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoAprovacao
        fields = ('id', 'nome')


class TipoRecursoSerializer(serializers.ModelSerializer):
    grupo = ApprovalGroupSummarySerializer()

    class Meta:
        model = TipoRecurso
        fields = '__all__'


class ResourceTypeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRecurso
        fields = ('id', 'name')






