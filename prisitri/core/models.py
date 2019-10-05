
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TipoRecurso(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Recurso(models.Model):
    tipo = models.ForeignKey(TipoRecurso, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, null=True, blank=True)

    @property
    def periodo(self):
        return f'{self.inicio} a {self.fim}'

    def recurso_esta_disponivel(self):
        # agendamentos_recurso = Agendamento.objects.filter(recurso=self.recurso.id)
        agendamentos = Agendamento.objects.filter(
            recurso=self.recurso.id,
            inicio__gte=self.inicio,
            # fim__lte=self.fim
        )
        print(agendamentos)
        return True
        # return agendamentos

    def __str__(self):
        return f'{self.recurso} - {self.periodo}'

    def clean(self):
        if not self.recurso_esta_disponivel():
            raise ValidationError(_('O recurso não está disponível no período.'))
