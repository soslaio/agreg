
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import Group


class TipoRecurso(models.Model):
    nome = models.CharField(max_length=200)
    grupo_aprovacao = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Grupo Gerentes')

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Recurso(models.Model):
    tipo = models.ForeignKey(TipoRecurso, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, default='pendente')

    class Meta:
        ordering = ['inicio']

    @property
    def inicio_formatado(self):
        return self.inicio.strftime('%d/%m/%Y')

    @property
    def fim_formatado(self):
        return self.fim.strftime('%d/%m/%Y')

    @property
    def periodo(self):
        return f'{self.inicio_formatado} a {self.fim_formatado}'

    @property
    def recurso_esta_disponivel(self):
        agendamentos = Agendamento.objects.filter(
            Q(inicio__range=(self.inicio, self.fim)) |
            Q(fim__range=(self.inicio, self.fim))
        ).exclude(pk=self.id)
        esta_disponivel = len(agendamentos) == 0
        return esta_disponivel

    def __str__(self):
        return f'{self.recurso} - {self.periodo}'

    def clean(self):
        if not self.recurso_esta_disponivel:
            raise ValidationError(_('O recurso não está disponível no período solicitado.'))
