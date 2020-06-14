
import uuid
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

exposed_request = None


class ExtendedUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarios', verbose_name='usuário do sistema')
    companies = models.ManyToManyField('Empresa', blank=True, verbose_name='empresas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name='ativo')

    class Meta:
        ordering = ['user']
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    @property
    def nome(self):
        return self.user.get_full_name() if self.user.first_name else self.user.username

    def __str__(self):
        return self.nome


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('ExtendedUser', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='proprietário')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name='ativo')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        extendeduser = ExtendedUser.objects.get(user__id=exposed_request.user.id)
        self.owner = extendeduser
        super().save(*args, **kwargs)


class Empresa(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class GrupoAprovacao(BaseModel):
    company = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='empresa')
    name = models.CharField(max_length=200, verbose_name='nome')

    class Meta:
        ordering = ['name']
        verbose_name = 'Grupo de aprovação'
        verbose_name_plural = 'Grupos de aprovação'

    def __str__(self):
        return self.name


class TipoRecurso(BaseModel):
    NATUREZAS = [
        ('humanos', 'Recursos Humanos'),
        ('materiais', 'Recursos Materiais')
    ]
    company = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    natureza = models.CharField(max_length=200, choices=NATUREZAS)
    grupo = models.ForeignKey(GrupoAprovacao, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Grupo de aprovação')

    class Meta:
        ordering = ['name', 'grupo', 'company']
        verbose_name = 'Tipo de recurso'
        verbose_name_plural = 'Tipos de recursos'

    @property
    def necessita_aprovacao(self):
        return self.grupo is not None

    def __str__(self):
        return f'{self.name} ({self.company})'


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
    description = models.TextField(null=True, blank=True, verbose_name='descrição')

    class Meta:
        ordering = ['nome']
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
        return f'{self.nome} ({self.tempo_unidade})'


class Recurso(BaseModel):
    name = models.CharField(max_length=200, null=True, blank=True,
                            help_text='No caso de recursos humanos, é o nome do profissional.')
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    quantity = models.IntegerField(default=1, verbose_name='quantidade')
    company = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    tipos_alocacao = models.ManyToManyField(TipoAlocacao, verbose_name='tipos de alocação')
    disponibilidade_inicio = models.TimeField()
    disponibilidade_fim = models.TimeField()

    class Meta:
        ordering = ['name']

    @property
    def tipo_recurso(self):
        return self.tipos_alocacao.first().tipo_recurso

    def __str__(self):
        return self.name or str(self.tipo_recurso)


class Alocacao(BaseModel):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='alocacoes')
    observacao = models.TextField(null=True, blank=True, verbose_name='observação')

    class Meta:
        ordering = ['recurso']
        verbose_name = 'Alocação'
        verbose_name_plural = 'Alocações'

    @property
    def aprovado(self):
        """Informa se todas as agendas da alocação foram aprovadas"""
        print(self.agenda_set.all())
        return False

    def __str__(self):
        return f'{self.recurso} para {self.solicitante.nome}'


class Agenda(BaseModel):
    STATUS = [
        ('aprovado', 'Aprovado'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado')
    ]
    alocacao = models.ForeignKey(Alocacao, on_delete=models.CASCADE, verbose_name='alocação')
    tipo_alocacao = models.ForeignKey(TipoAlocacao, on_delete=models.CASCADE, verbose_name='tipo de alocação')
    inicio = models.DateTimeField(verbose_name='início')
    termino = models.DateTimeField(verbose_name='término')
    status = models.CharField(max_length=200, choices=STATUS)

    def __str__(self):
        return f'{self.alocacao}: {self.tipo_alocacao}'


@receiver(post_save, sender=User)
def create_extendeduser(sender, instance, created, **kwargs):
    if created:
        ExtendedUser.objects.create(user=instance)




