from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.html import format_html

# Register your models here.
from .models import TipoRecurso, Recurso, Agendamento

admin.site.register(TipoRecurso)


@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'nome', 'descricao', 'ativo')


# def html_status(self):
#     return self.

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    date_hierarchy = 'inicio'
    list_display = ('recurso', 'periodo', 'solicitante', 'html_status')
    fields = ('recurso', 'inicio', 'fim')
    list_filter = ('status',)
    actions = ['aprovar', 'reprovar']

    def html_status(self, obj):
        icone = {
            'pendente': 'icon-unknown',
            'aprovado': 'icon-yes',
            'reprovado': 'icon-no'
        }
        return format_html(
            '<img src="/static/admin/img/{}.svg" alt="True">',
            icone[obj.status]
        )
    html_status.short_description = 'status'

    def aprovar(self, request, queryset):
        queryset.update(status='aprovado')

    def reprovar(self, request, queryset):
        queryset.update(status='reprovado')

    def save_model(self, request, obj, form, change):
        obj.solicitante = request.user  # registra o solicitante logado
        super().save_model(request, obj, form, change)
