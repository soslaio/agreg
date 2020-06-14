
from django.contrib import admin
from .models import Empresa, GrupoAprovacao, TipoRecurso, Recurso, TipoAlocacao, Alocacao, ExtendedUser, Agenda


class BaseAdmin(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        exclude = ['owner']
        if not obj:
            exclude.append('active')
        return exclude

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('id',)
        if obj:
            self.readonly_fields += ('owner',)
        return self.readonly_fields


@admin.register(Empresa)
class EmpresaAdmin(BaseAdmin):
    list_display = ('id', 'name', 'active')


@admin.register(ExtendedUser)
class UsuarioAdmin(BaseAdmin):
    list_display = ('id', 'nome')
    filter_horizontal = ('companies',)

    def nome(self, obj):
        return obj.nome


@admin.register(Recurso)
class RecursoAdmin(BaseAdmin):
    list_display = ('id', 'name', 'tipo_recurso', 'company', 'quantity')

    def tipo_recurso(self, obj):
        return obj.tipo_recurso


@admin.register(GrupoAprovacao)
class GrupoAprovacaoAdmin(BaseAdmin):
    list_display = ('id', 'name', 'company')


@admin.register(TipoRecurso)
class TipoRecursoAdmin(BaseAdmin):
    list_display = ('name', 'grupo', 'company')
    list_filter = ('natureza', 'grupo', 'company')


@admin.register(TipoAlocacao)
class TipoAlocacaoAdmin(BaseAdmin):
    list_display = ('nome', 'get_tipo_recurso', 'tempo_unidade')
    list_filter = ('tipo_recurso',)

    def get_tipo_recurso(self, obj):
        return obj.tipo_recurso.name
    get_tipo_recurso.short_description = 'Tipo de produto'

    def tempo_unidade(self, obj):
        return obj.tempo_unidade
    tempo_unidade.short_description = 'Tempo'


@admin.register(Alocacao)
class AlocacaoAdmin(BaseAdmin):
    list_display = ('id', 'recurso', 'solicitante', 'aprovado')

    def aprovado(self, obj):
        return obj.aprovado

    aprovado.boolean = True


@admin.register(Agenda)
class AgendaAdmin(BaseAdmin):
    list_display = ('id', 'tipo_alocacao', 'inicio', 'termino')
    list_filter = ('tipo_alocacao',)


