
from django.contrib import admin
from .models import Company, ApprovalGroup, ResourceType, Resource, ScheduleType, Order, ExtendedUser, Schedule


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
    list_display = ('id', 'name', 'is_active')


@admin.register(ExtendedUser)
class ExtendedUserAdmin(BaseAdmin):
    list_display = ('id', 'nome')
    filter_horizontal = ('companies',)

    def nome(self, obj):
        return obj.nome


@admin.register(Resource)
class ResourceAdmin(BaseAdmin):
    list_display = ('id', 'name', 'tipo_recurso', 'company', 'quantity')
    filter_horizontal = ('schedule_types',)

    def tipo_recurso(self, obj):
        return obj.tipo_recurso


@admin.register(ApprovalGroup)
class ApprovalGroupAdmin(BaseAdmin):
    list_display = ('id', 'name', 'company')


@admin.register(ResourceType)
class ResourceTypeAdmin(BaseAdmin):
    list_display = ('name', 'approval_group', 'company')
    list_filter = ('nature', 'approval_group', 'company')


@admin.register(ScheduleType)
class ScheduleTypeAdmin(BaseAdmin):
    list_display = ('name', 'get_resource_type', 'time_unit')
    list_filter = ('resource_type',)

    def get_resource_type(self, obj):
        return obj.resource_type.name
    get_resource_type.short_description = 'Tipo de produto'

    def time_unit(self, obj):
        return obj.time_unit
    time_unit.short_description = 'Tempo'


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ('id', 'recurso', 'solicitante', 'aprovado')

    def aprovado(self, obj):
        return obj.aprovado

    aprovado.boolean = True


@admin.register(Schedule)
class ScheduleAdmin(BaseAdmin):
    list_display = ('id', 'tipo_alocacao', 'inicio', 'termino')
    list_filter = ('tipo_alocacao',)


