
from django.contrib import admin
from .models import Empresa, GrupoAprovacao, TipoRecurso, Recurso, TipoAlocacao, Alocacao, Usuario, Agenda


admin.site.register(Empresa)


class BaseAdmin(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        if not obj:
            return ('ativo',)


@admin.register(Usuario)
class UsuarioAdmin(BaseAdmin):
    list_display = ('id', 'empresa', 'nome')

    def nome(self, obj):
        return obj.nome


@admin.register(Recurso)
class RecursoAdmin(BaseAdmin):
    list_display = ('id', 'nome', 'tipo_recurso', 'empresa', 'quantidade')

    def tipo_recurso(self, obj):
        return obj.tipo_recurso


@admin.register(GrupoAprovacao)
class GrupoAprovacaoAdmin(BaseAdmin):
    list_display = ('id', 'nome', 'empresa')


@admin.register(TipoRecurso)
class TipoRecursoAdmin(BaseAdmin):
    list_display = ('id', 'nome', 'grupo')
    list_filter = ('natureza', 'grupo', 'empresa')


@admin.register(TipoAlocacao)
class TipoAlocacaoAdmin(BaseAdmin):
    list_display = ('id', 'tipo_recurso', 'nome', 'tempo_unidade')
    list_filter = ('tipo_recurso',)

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


