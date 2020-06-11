
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Empresa, TipoRecurso, Usuario


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class TipoRecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRecurso
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    empresa = EmpresaSerializer()

    class Meta:
        model = Usuario
        fields = '__all__'




