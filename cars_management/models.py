from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_service = models.BooleanField(default=False, blank=True, verbose_name='Является сотрудником сервисной компании')
    service_company = models.ForeignKey(to='ServiceCompany', blank=True, null=True, on_delete=models.PROTECT,
                                        verbose_name='Сервисная компания')

    def __str__(self):
        return f'{self.user.username} {self.is_service}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class ServiceCompany(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Technics(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'technics'

    def __str__(self):
        return f'{self.name}'


class EngineModels(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'engine_models'

    def __str__(self):
        return f'{self.name}'


class TransmissionModels(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'transmission_models'

    def __str__(self):
        return f'{self.name}'


class SteeringAxleType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'front_axle_models'

    def __str__(self):
        return f'{self.name}'

class DriveAxleType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'rear_axle_models'

    def __str__(self):
        return f'{self.name}'


class MaintenanceType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'maintenance_types'

    def __str__(self):
        return f'{self.name}'

class FailureNodes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'failure_nodes'

    def __str__(self):
        return f'{self.name}'


class RestorationMethods(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'restoration_methods'

    def __str__(self):
        return f'{self.name}'


class Car(models.Model):
    factory_number = models.CharField(unique=True, max_length=15, verbose_name= 'Зав. № машины')
    model = models.ForeignKey(Technics, on_delete=models.CASCADE, verbose_name='Модель техники')
    engine_type = models.ForeignKey(EngineModels, on_delete=models.CASCADE, verbose_name='Модель двигателя')
    engine_id = models.CharField(max_length=255, verbose_name='Зав. № двигателя')
    transmission_type = models.ForeignKey(TransmissionModels, on_delete=models.CASCADE, verbose_name='Модель трансмиссии')
    transmission_id = models.CharField(max_length=255, verbose_name='Зав. № трансмиссии')
    drive_axle_type = models.ForeignKey(DriveAxleType, on_delete=models.CASCADE, verbose_name='Модель ведущего моста')
    drive_axle_id = models.CharField(max_length=255, verbose_name='Зав. № ведущего моста')
    steering_axle_type = models.ForeignKey(SteeringAxleType, on_delete=models.CASCADE, verbose_name='Модель управляемого моста')
    steering_axle_id = models.CharField(max_length=255, verbose_name='Зав. № управляемого моста')
    supply_contract_data = models.CharField(max_length=255, verbose_name='№ и дата договора поставки')
    shipment_date = models.DateField(default=timezone.now, verbose_name='Дата отгрузки с завода')
    consignee = models.CharField(max_length=255, verbose_name='Грузополучатель (конечный потребитель)')
    consignee_address = models.CharField(max_length=255, verbose_name='Адрес грузополучателя')
    car_config = models.CharField(max_length=255, verbose_name='Комплектация и доп. опции', default='Стандарт')
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    class Meta:
        ordering = ['shipment_date']

    def __str__(self):
        return f'{self.factory_number}'


class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE, verbose_name='Вид техобслуживания')
    maintenance_date = models.DateField(default=timezone.now, verbose_name='Дата проведения ТО')
    operating_hours = models.DecimalField(max_digits=10, decimal_places=0, default=0,  verbose_name='Наработка, м/час')
    work_order_number = models.CharField(max_length=255, verbose_name='№ заказ-наряда')
    work_order_date = models.DateField(default=timezone.now, verbose_name='Дата заказ-наряда')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Сервисная организация, проводившая ТО')

    class Meta:
        ordering = ['maintenance_date']
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Технические обслуживания'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.maintenance_date} {self.car}'


class Reclamation(models.Model):
    date_of_failure = models.DateField(default=timezone.now, verbose_name='Дата отказа')
    operating_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Наработка, м/час')
    failure_node = models.ForeignKey(FailureNodes, on_delete=models.CASCADE, verbose_name='Узел отказа')
    failure_description = models.TextField(blank=True, null=True, verbose_name='Описание отказа')
    restoration_method = models.ForeignKey(RestorationMethods, on_delete=models.CASCADE, verbose_name='Способ восстановления')
    used_spare_parts = models.TextField(blank=True, null=True, verbose_name='Используемые запчасти')
    restoration_date = models.DateField(default=timezone.now, verbose_name='Дата восстановления')
    downtime_hours = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Время простоя техники, час', blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    def __str__(self):
        return f'{self.date_of_failure} {self.car}'

    class Meta:
        ordering = ['date_of_failure']
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'

    def save(self, *args, **kwargs):
        self.downtime_hours = (self.restoration_date - self.date_of_failure).total_seconds() / 3600
        super().save(*args, **kwargs)