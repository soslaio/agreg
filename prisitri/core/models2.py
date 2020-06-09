
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import Group


# class Empresa(models.Model):
#     nome = models.CharField(max_length=200)
#     endereco = models.CharField(max_length=200)
#     contatos = models.CharField(max_length=200)
#
#     class Meta:
#         ordering = ['nome']
#
#     def __str__(self):
#         return self.nome


class BaseModel(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TipoRecurso(BaseModel):
    nome = models.CharField(max_length=200)
    grupo_aprovacao = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Grupo Gerentes', related_name='tiposrecurso')

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Recurso(BaseModel):
    tipo = models.ForeignKey(TipoRecurso, on_delete=models.CASCADE, related_name='recursos')
    nome = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Agendamento(BaseModel):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name='agendamentos')
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos')
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
