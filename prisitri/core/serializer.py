
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Empresa, TipoRecurso, Usuario, GrupoAprovacao


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class GrupoAprovacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoAprovacao
        fields = '__all__'


class TipoRecursoSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    grupo = GrupoAprovacaoSerializer()

    class Meta:
        model = TipoRecurso
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    empresas = EmpresaSerializer(many=True)

    class Meta:
        model = Usuario
        fields = '__all__'




