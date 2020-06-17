
import uuid
from django.db import models
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.admin.utils import flatten

exposed_request = None


class ExtendedUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarios', verbose_name='usuário do sistema')
    companies = models.ManyToManyField('Company', blank=True, verbose_name='empresas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='ativo')

    class Meta:
        ordering = ['user']
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    @property
    def name(self):
        return self.user.get_full_name() if self.user.first_name else self.user.username

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


class Company(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Empresa'

    def __str__(self):
        return self.name


class ApprovalGroup(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='empresa')
    name = models.CharField(max_length=200, verbose_name='nome')

    class Meta:
        ordering = ['name']
        verbose_name = 'Grupo de aprovação'
        verbose_name_plural = 'Grupos de aprovação'

    def __str__(self):
        return self.name


class ResourceType(BaseModel):
    NATUREZAS = [
        ('humanos', 'Recursos Humanos'),
        ('materiais', 'Recursos Materiais')
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='empresa')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    nature = models.CharField(max_length=200, choices=NATUREZAS)
    approval_group = models.ForeignKey(ApprovalGroup, on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name='Grupo de aprovação')

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
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    time = models.IntegerField()
    unit = models.CharField(max_length=200, choices=UNIDADES, default='minutes')
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
    name = models.CharField(max_length=200, null=True, blank=True,
                            help_text='No caso de recursos humanos, é o nome do profissional.')
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    quantity = models.IntegerField(default=1, verbose_name='quantidade')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='empresa')
    schedule_types = models.ManyToManyField(ScheduleType, verbose_name='tipos de alocação')

    class Meta:
        ordering = ['name']
        verbose_name = 'Recurso'

    # def __getall_availabilities(self, schedule_type, date):
    #     date_obj = datetime.strptime(date, '%Y-%m-%d')
    #     delta = schedule_type.get_time_delta()
    #     limit = datetime.combine(date_obj, self.available_until)
    #     all_availabilities = []
    #     start = datetime.combine(date_obj, self.available_from)
    #     end = start + delta
    #
    #     while True:
    #         if end > limit:
    #             break
    #         all_availabilities.append({'start': start, 'end': end})
    #         start = end
    #         end = end + delta
    #
    #     return all_availabilities
    #
    # def get_availability(self, schedule_type: ScheduleType, date: str):
    #     all_availabilities = self.__getall_availabilities(schedule_type, date)
    #     return all_availabilities

    def __get_slots_in_availability(self, availability_start, availability_end, delta):
        slots = []
        start = availability_start
        end = start + delta

        while True:
            if end > availability_end:
                break
            slots.append({'start': start, 'end': end})
            start = end
            end = end + delta

        return slots

    def get_availability(self, schedule_type: ScheduleType, date: str):
        availabilities = self.availability_set.all()
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        delta = schedule_type.get_time_delta()
        slots = []
        for availability in availabilities:
            start = datetime.combine(date_obj, availability.start)
            end = datetime.combine(date_obj, availability.end)
            availability_slots = self.__get_slots_in_availability(start, end, delta)
            slots.append(availability_slots)

        return flatten(slots)

    def get_schedules(self, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        orders = self.order_set.filter(resource__id=self.id)
        orders_ids = set(orders.values_list('id', flat=True))
        schedules = Schedule.objects.filter(order__id__in=orders_ids).filter(start__date=date_obj)
        return schedules

    def __str__(self):
        return self.name or self.resource_type.name


class Availability(BaseModel):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='recurso')
    start = models.TimeField(verbose_name='início')
    end = models.TimeField(verbose_name='término')

    class Meta:
        ordering = ['resource', 'start']

    def __str__(self):
        return f'{self.resource} das {self.start} às {self.end}'


class Order(BaseModel):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='recurso')
    requester = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='alocacoes',
                                  verbose_name='solicitante')
    notes = models.TextField(null=True, blank=True, verbose_name='observação')

    class Meta:
        ordering = ['resource']
        verbose_name = 'Alocação'
        verbose_name_plural = 'Alocações'

    @property
    def approved(self):
        """Informa se todas as agendas da alocação foram aprovadas"""
        return False

    def __str__(self):
        return f'{self.resource} para {self.requester.name}'


class Schedule(BaseModel):
    STATUS = [
        ('aprovado', 'Aprovado'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado')
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='alocação')
    start = models.DateTimeField(verbose_name='início')
    end = models.DateTimeField(verbose_name='término')
    status = models.CharField(max_length=200, choices=STATUS)

    class Meta:
        ordering = ['order', 'start', 'end']
        verbose_name = 'Agenda'

    def __str__(self):
        return f'{self.order}: {self.start}'


@receiver(post_save, sender=User)
def create_extendeduser(sender, instance, created, **kwargs):
    if created:
        ExtendedUser.objects.create(user=instance)

