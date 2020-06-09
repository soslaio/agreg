
from django.db import models


class BaseModel(models.Model):
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Empresa(BaseModel):
    nome = models.CharField(max_length=200)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class TipoRecurso(BaseModel):
    nome = models.CharField(max_length=200)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Recurso(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, null=True, blank=True)
    quantidade = models.IntegerField(default=1)
    disponibilidade_inicio = models.TimeField()
    disponibilidade_fim = models.TimeField()


class TipoAlocacao(BaseModel):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    tempo = models.TimeField()


class Alocacao(BaseModel):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    observacao = models.TextField()


class Agenda(BaseModel):
    tipo_alocacao = models.ForeignKey(TipoAlocacao, on_delete=models.CASCADE)
    data = models.DateField()
    inicio = models.DateTimeField()
    termino = models.DateTimeField()


