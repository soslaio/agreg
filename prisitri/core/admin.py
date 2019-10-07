
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import TipoRecurso, Recurso, Agendamento, Empresa
from django.http import HttpResponseRedirect


class SemTodosSimpleListFilter(admin.SimpleListFilter):
    def choices(self, changelist):
        """Este método foi sobrescrito para poder retirar a opção 'Todos'."""
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
            'display': _('Pendentes'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


class StatusFilter(SemTodosSimpleListFilter):
    title = _('status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('aprovado', 'Aprovados'),
            ('reprovado', 'Reprovados'),
            ('todos', 'Todos')
        )

    def queryset(self, request, queryset):

        if not request.user.is_superuser:
            grupos_usuario = [g.id for g in request.user.groups.all()]
            tipos_recurso = [t.id for t in TipoRecurso.objects.filter(grupo_aprovacao__in=grupos_usuario)]
            recursos = [r.id for r in Recurso.objects.filter(tipo__in=tipos_recurso)]
            queryset = Agendamento.objects.filter(recurso__in=recursos)

        if self.value() == 'aprovado':
            return queryset.filter(status='aprovado')
        elif self.value() == 'reprovado':
            return queryset.filter(status='reprovado')
        elif self.value() == 'pendente':
            return queryset.filter(status='pendente')
        elif self.value() == 'todos':
            return queryset.all()
        elif self.value() is None:
            return queryset.filter(status='pendente')


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(TipoRecurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo_aprovacao')
    list_filter = ('grupo_aprovacao',)


@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'ativo')
    list_filter = ('tipo', 'ativo')


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    change_form_template = "agendamento_changeform.html"
    date_hierarchy = 'inicio'
    list_display = ('recurso', 'periodo', 'solicitante', 'html_status')
    fields = ('recurso', 'inicio', 'fim')
    list_filter = (StatusFilter,)
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

    def response_change(self, request, obj):
        if "_aprovar" in request.POST:
            obj.status = 'aprovado'
            obj.save()
            self.message_user(request, "O agendamento foi aprovado com sucesso.")
            return HttpResponseRedirect(".")
        if "_cancelar" in request.POST:
            obj.status = 'reprovado'
            obj.save()
            self.message_user(request, "O agendamento foi cancelado com sucesso.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def aprovar(self, request, queryset):
        queryset.update(status='aprovado')

    def reprovar(self, request, queryset):
        queryset.update(status='reprovado')

    def save_model(self, request, obj, form, change):
        obj.solicitante = request.user  # registra o solicitante logado
        super().save_model(request, obj, form, change)

    html_status.short_description = 'status'
