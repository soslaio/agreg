from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError

# Register your models here.
from .models import TipoRecurso, Recurso, Agendamento

admin.site.register(TipoRecurso)


@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'nome', 'descricao')


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('recurso', 'periodo', 'solicitante', 'status')
    fields = ('recurso', 'inicio', 'fim')
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):
        obj.solicitante = request.user  # registra o solicitante logado
        super().save_model(request, obj, form, change)
