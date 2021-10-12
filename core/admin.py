
from django.contrib import admin
from .models import (
    Company,
    ApprovalGroup,
    ResourceType,
    Resource,
    ScheduleType,
    Order,
    ExtendedUser,
    Schedule,
    Availability,
    CompanyType,
    Unit
)


admin.site.register(CompanyType)
admin.site.register(Unit)


class AvailabilityInline(admin.TabularInline):
    extra = 1
    model = Availability
    exclude = ('owner', 'is_active')


class ScheduleInline(admin.TabularInline):
    model = Schedule
    exclude = ('owner', 'is_active')


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
    list_display = ('id', 'name', 'company_type', 'slug', 'is_active')
    list_filter = ('company_type', 'is_active')


@admin.register(Schedule)
class ScheduleAdmin(BaseAdmin):
    list_display = ('id', 'resource', 'start', 'end', 'status')
    list_filter = ('resource', 'status')


@admin.register(ExtendedUser)
class ExtendedUserAdmin(BaseAdmin):
    list_display = ('id', 'name')
    filter_horizontal = ('companies', 'approval_groups')


@admin.register(Resource)
class ResourceAdmin(BaseAdmin):
    list_display = ('name_or_rt_name', 'resource_type', 'unit', 'quantity')
    filter_horizontal = ('schedule_types',)
    inlines = [AvailabilityInline]

    def get_exclude(self, request, obj=None):
        """Desativa o campo de aprovação do recurso caso o tipo de recurso não precise de aprovação"""
        if obj and not obj.resource_type.needs_approval:
            self.exclude = ['needs_approval']
        return self.exclude


@admin.register(ApprovalGroup)
class ApprovalGroupAdmin(BaseAdmin):
    list_display = ('id', 'name', 'unit')


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
    list_display = ('id', 'requester', 'approved')
    inlines = [ScheduleInline]

    def approved(self, obj):
        return obj.approved
    approved.boolean = True
    approved.short_description = 'aprovado?'
