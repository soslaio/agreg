
from django.db import models
from django.contrib.auth.models import User


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


class Usuario(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        ordering = ['empresa', 'user']
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.user.username


class GrupoAprovacao(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Grupo de aprovação'
        verbose_name_plural = 'Grupos de aprovação'

    def __str__(self):
        return self.nome


class TipoRecurso(BaseModel):
    NATUREZAS = [
        ('humanos', 'Humanos'),
        ('materiais', 'Materiais')
    ]
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True, verbose_name='descrição')
    natureza = models.CharField(max_length=200, choices=NATUREZAS)
    grupo = models.ForeignKey(GrupoAprovacao, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Grupo de aprovação')

    class Meta:
        ordering = ['nome']
        verbose_name = 'Tipo de recurso'
        verbose_name_plural = 'Tipos de recursos'

    @property
    def necessita_aprovacao(self):
        return self.grupo is not None

    def __str__(self):
        return self.nome


class TipoAlocacao(BaseModel):
    UNIDADES = [
        ('minutos', 'Minutos'),
        ('horas', 'Horas'),
        ('dias', 'Dias'),
        ('semanas', 'Semanas'),
        ('meses', 'Meses'),
        ('anos', 'Anos')
    ]
    tipo_recurso = models.ForeignKey(TipoRecurso, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    tempo = models.IntegerField()
    unidade = models.CharField(max_length=200, choices=UNIDADES, default='minutos')
    descricao = models.TextField(null=True, blank=True, verbose_name='descrição')

    class Meta:
        ordering = ['tipo_recurso', 'nome']
        verbose_name = 'Tipo de alocação'
        verbose_name_plural = 'Tipos de alocação'

    @property
    def tempo_unidade(self):
        if self.tempo == 1:
            if self.unidade != 'meses':
                return f'{self.tempo} {self.unidade[:-1]}'
            else:
                return f'{self.tempo} mês'
        return f'{self.tempo} {self.unidade}'

    def __str__(self):
        return self.nome


class Recurso(BaseModel):
    nome = models.CharField(max_length=200, null=True, blank=True,
                            help_text='No caso de recursos humanos, é o nome do profissional.')
    descricao = models.TextField(null=True, blank=True, verbose_name='descrição')
    quantidade = models.IntegerField(default=1)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    tipos_alocacao = models.ManyToManyField(TipoAlocacao, verbose_name='tipos de alocação')
    disponibilidade_inicio = models.TimeField()
    disponibilidade_fim = models.TimeField()

    class Meta:
        ordering = ['nome']

    @property
    def tipo_recurso(self):
        return self.tipos_alocacao.first().tipo_recurso

    def __str__(self):
        return self.nome or f'{self.tipo_recurso}#{self.quantidade}'


class Alocacao(BaseModel):
    STATUS = [
        ('aprovado', 'Aprovado'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado')
    ]
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True, verbose_name='observação')
    status = models.CharField(max_length=200, choices=STATUS)

    class Meta:
        ordering = ['recurso', 'status']
        verbose_name = 'Alocação'
        verbose_name_plural = 'Alocações'

    def __str__(self):
        return f'{self.recurso} para {self.solicitante.user.username}'


class Agenda(BaseModel):
    tipo_alocacao = models.ForeignKey(TipoAlocacao, on_delete=models.CASCADE)
    data = models.DateField()
    inicio = models.DateTimeField()
    termino = models.DateTimeField()




