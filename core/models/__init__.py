
import uuid
from django.db import models
from datetime import datetime, timedelta
from django.db.models import Q
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.contrib.admin.utils import flatten
from multiselectfield import MultiSelectField

exposed_request = None


class ExtendedUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarios', verbose_name='usuário do sistema')
    companies = models.ManyToManyField('Company', blank=True, verbose_name='empresas')
    approval_groups = models.ManyToManyField('ApprovalGroup', blank=True, verbose_name='empresas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='ativo')

    class Meta:
        ordering = ['user']
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def name(self):
        return self.user.get_full_name() if self.user.first_name else self.user.username
    name.short_description = "nome"
    name = property(name)

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('ExtendedUser', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='proprietário')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='ativo')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        extendeduser = ExtendedUser.objects.get(user__id=exposed_request.user.id)
        self.owner = extendeduser
        super().save(*args, **kwargs)


class CompanyType(BaseModel):
    name = models.CharField(max_length=200, verbose_name='nome')
    slug = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tipo de Empresa'
        verbose_name_plural = 'Tipos de Empresa'

    def __str__(self):
        return self.name


class Company(BaseModel):
    name = models.CharField(max_length=200, verbose_name='nome')
    company_type = models.ForeignKey('CompanyType', on_delete=models.CASCADE, verbose_name='tipo de empresa')
    logo = models.ImageField(upload_to='companies/', blank=True, null=True, verbose_name='logo')
    slug = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Empresa'

    def __str__(self):
        return self.name


class Unit(BaseModel):
    name = models.CharField(max_length=200, verbose_name='nome')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='empresa')

    class Meta:
        ordering = ['name']
        verbose_name = 'Unidade/Filial'
        verbose_name_plural = "Unidades/Filiais"

    def __str__(self):
        return self.name


class ApprovalGroup(BaseModel):
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, verbose_name='unidade')
    name = models.CharField(max_length=200, verbose_name='nome')

    class Meta:
        ordering = ['name']
        verbose_name = 'Grupo de Aprovação'
        verbose_name_plural = 'Grupos de Aprovação'

    def __str__(self):
        return self.name


class ResourceType(BaseModel):
    NATUREZAS = [
        ('human', 'Recursos Humanos'),
        ('material', 'Recursos Materiais')
    ]
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='empresa')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    nature = models.CharField(max_length=200, choices=NATUREZAS, verbose_name='natureza')
    approval_group = models.ForeignKey(ApprovalGroup, on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name='Grupo de aprovação')
    image = models.ImageField(upload_to='resource_types/', blank=True, null=True, verbose_name='imagem')

    class Meta:
        ordering = ['name', 'approval_group', 'company']
        verbose_name = 'Tipo de recurso'
        verbose_name_plural = 'Tipos de recursos'

    @property
    def needs_approval(self):
        return self.approval_group is not None

    @property
    def resources(self):
        return self.resource_set.all()

    def __str__(self):
        return f'{self.name} ({self.company})'


class ScheduleType(BaseModel):
    UNIDADES = [
        ('minutes', 'Minutos'),
        ('hours', 'Horas'),
        ('days', 'Dias'),
        ('weeks', 'Semanas'),
        ('months', 'Meses'),
        ('years', 'Anos')
    ]
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE, verbose_name='tipo')
    name = models.CharField(max_length=200, verbose_name='nome')
    time = models.IntegerField(verbose_name='tempo')
    unit = models.CharField(max_length=200, choices=UNIDADES, default='minutes', verbose_name='unidade')
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    available_from = models.TimeField(verbose_name='disponível de')
    available_until = models.TimeField(verbose_name='disponível até')

    class Meta:
        ordering = ['name']
        verbose_name = 'Tipo de agenda'
        verbose_name_plural = 'Tipos de agendas'

    def get_time_delta(self):
        return eval(f'timedelta({self.unit}={self.time})')

    @property
    def time_unit(self):
        if self.time == 1:
            if self.unit != 'months':
                return f'{self.time} {self.unit[:-1]}'
            else:
                return f'{self.time} mês'
        return f'{self.time} {self.unit}'

    def __str__(self):
        return f'{self.name} ({self.time_unit})'


class Resource(BaseModel):
    resource_type = models.ForeignKey(ResourceType, models.CASCADE, verbose_name='tipo')
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='nome',
                            help_text='No caso de recursos humanos, é o nome do profissional.')
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    quantity = models.IntegerField(default=1, verbose_name='quantidade')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='empresa')
    schedule_types = models.ManyToManyField(ScheduleType, verbose_name='tipos de alocação')
    needs_approval = models.BooleanField(null=True, blank=True, verbose_name='necessita aprovação')

    class Meta:
        ordering = ['name']
        verbose_name = 'Recurso'

    def get_needs_approval(self):
        return self.needs_approval if self.needs_approval else self.resource_type.needs_approval

    def __get_schedules(self, date_obj):
        orders = self.order_set.all()
        orders_ids = set(orders.values_list('id', flat=True))
        schedules = Schedule.objects.filter(order__id__in=orders_ids).filter(start__date=date_obj)
        return schedules

    def __get_slots_in_availability(self, availability_start, availability_end, delta, schedules):
        slots = []
        start = availability_start
        end = start + delta

        while end <= availability_end:
            slot_schedules = schedules.filter(
                Q(start__gte=start, start__lt=end) |
                Q(end__gt=start, end__lte=end) |
                Q(start__lt=start, end__gt=end)
            )

            if not slot_schedules.count() > 0:
                slots.append({'start': start, 'end': end})
                start = end
            else:
                last_schedule = slot_schedules.last()
                start = last_schedule.end.astimezone(None).replace(tzinfo=None)

            end = start + delta
        return slots

    def get_availability(self, schedule_type: ScheduleType, date: str):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        availabilities = self.availability_set.all()
        schedules = self.__get_schedules(date_obj)
        delta = schedule_type.get_time_delta()
        slots = []
        for availability in availabilities:
            start = datetime.combine(date_obj, availability.start)
            end = datetime.combine(date_obj, availability.end)
            availability_slots = self.__get_slots_in_availability(start, end, delta, schedules)
            slots.append(availability_slots)

        return flatten(slots)

    def get_schedules(self, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        schedules = self.__get_schedules(date_obj)
        return schedules

    def __name_or_rt_name(self):
        return self.name or f'{self.resource_type.name} ({self.quantity})'
    __name_or_rt_name.short_description = "nome"
    name_or_rt_name = property(__name_or_rt_name)

    def __str__(self):
        return self.name or self.resource_type.name


class Availability(BaseModel):
    WEEKDAYS = [
        (0, 'Domingo'),
        (1, 'Segunda'),
        (2, 'Terça'),
        (3, 'Quarta'),
        (4, 'Quinta'),
        (5, 'Sexta'),
        (6, 'Sábado')
    ]
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='recurso')
    weekdays = MultiSelectField(choices=WEEKDAYS, default=[1, 2, 3, 4, 5], verbose_name='dias da semana')
    start = models.TimeField(verbose_name='início')
    end = models.TimeField(verbose_name='término')

    class Meta:
        ordering = ['resource', 'start']
        verbose_name = 'Horário Disponível'
        verbose_name_plural = 'Horários Disponíveis'

    def __str__(self):
        return f'{self.resource} das {self.start} às {self.end}'


class Order(BaseModel):
    requester = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='alocacoes',
                                  verbose_name='solicitante')
    notes = models.TextField(null=True, blank=True, verbose_name='observação')

    class Meta:
        ordering = ['requester']
        verbose_name = 'Alocação'
        verbose_name_plural = 'Alocações'

    @property
    def schedules(self):
        return self.schedule_set.all()

    @property
    def status(self):
        statuses = [s.status for s in self.schedules]
        if 'pending' in statuses:
            if all([s == 'pending' for s in statuses]):
                return 'pending'
            return 'waiting_approval'

        if 'approved' in statuses:
            if all([s == 'approved' for s in statuses]):
                return 'approved'
            return 'partially_approved'

        return 'canceled'

    @property
    def approved(self):
        """Informa se todas as agendas da alocação foram aprovadas"""
        return self.status == 'approved'

    def __str__(self):
        return f'{self.requester.name}'


class Schedule(BaseModel):
    STATUS = [
        ('approved', 'Aprovado'),
        ('pending', 'Pendente'),
        ('canceled', 'Cancelado')
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='alocação')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='recurso')
    start = models.DateTimeField(verbose_name='início')
    end = models.DateTimeField(verbose_name='término')
    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS)

    class Meta:
        ordering = ['order', 'start', 'end']
        verbose_name = 'Agenda'

    def __resource_needs_approval(self):
        return

    def __str__(self):
        return f'{self.order}: {self.start}'


@receiver(pre_save, sender=Schedule)
def set_schedule_status(instance, **kwargs):
    if not instance.status:
        instance.status = 'pending' if instance.resource.get_needs_approval() else 'approved'


@receiver(post_save, sender=User)
def create_extendeduser(sender, instance, created, **kwargs):
    if created:
        ExtendedUser.objects.create(user=instance)

