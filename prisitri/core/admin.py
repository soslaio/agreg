
from django.contrib import admin
from .models import Company, ApprovalGroup, ResourceType, Resource, TipoAlocacao, Alocacao, ExtendedUser, Agenda


class BaseAdmin(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        self.exclude = ['owner']
        if not obj:
            self.exclude.append('active')
        return self.exclude

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('id',)
        if obj:
            if hasattr(obj, 'owner'):
                self.readonly_fields += ('owner',)
        return self.readonly_fields


@admin.register(Company)
class CompanyAdmin(BaseAdmin):
    list_display = ('id', 'name', 'active')


@admin.register(ExtendedUser)
class ExtendedUserAdmin(BaseAdmin):
    list_display = ('id', 'nome')
    filter_horizontal = ('companies',)

    def nome(self, obj):
        return obj.nome


@admin.register(Resource)
class ResourceAdmin(BaseAdmin):
    list_display = ('id', 'name', 'tipo_recurso', 'company', 'quantity')

    def tipo_recurso(self, obj):
        return obj.tipo_recurso


@admin.register(ApprovalGroup)
class ApprovalGroupAdmin(BaseAdmin):
    list_display = ('id', 'name', 'company')


@admin.register(ResourceType)
class ResourceTypeAdmin(BaseAdmin):
    list_display = ('name', 'grupo', 'company')
    list_filter = ('natureza', 'grupo', 'company')


@admin.register(TipoAlocacao)
class TipoAlocacaoAdmin(BaseAdmin):
    list_display = ('name', 'get_tipo_recurso', 'tempo_unidade')
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


