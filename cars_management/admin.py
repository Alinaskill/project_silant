from django.contrib import admin
from .models import *
from import_export.admin import ImportExportMixin
from import_export import resources
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class TypeMaintenanceResource(resources.ModelResource):
    class Meta:
        model = MaintenanceType
        report_skipped = True
        fields = ('id','name','description',)


@admin.register(MaintenanceType)
class TypeMaintenanceAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = TypeMaintenanceResource
    list_display = ('id','name','description',)
    filter = ('name',)


class FailureResource(resources.ModelResource):
    class Meta:
        model = FailureNodes
        report_skipped = True
        fields = ('id','name','description',)


@admin.register(FailureNodes)
class FailureAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = FailureResource
    list_display = ('id','name','description',)
    filter = ('name',)


class RecoveryMethodResource(resources.ModelResource):
    class Meta:
        model = RestorationMethods
        report_skipped = True
        fields = ('id','name','description',)


@admin.register(RestorationMethods)
class RecoveryMethodAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = RecoveryMethodResource
    list_display = ('id','name','description',)
    filter = ('name',)


class ServiceCompanyResource(resources.ModelResource):
    class Meta:
        model = ServiceCompany
        report_skipped = True
        fields = ('id','name','description',)


@admin.register(ServiceCompany)
class ServiceCompanyAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = ServiceCompanyResource
    list_display = ('id','name','description',)
    filter = ('name',)


class MaintenanceResource(resources.ModelResource):
    class Meta:
        model = Maintenance
        report_skipped = True
        fields = ('id','maintenance_type','maintenance_date','operating_hours','work_order_number','work_order_date','service_company','car')


@admin.register(Maintenance)
class MaintenanceAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = MaintenanceResource
    list_display = ('id','maintenance_type','maintenance_date','operating_hours','work_order_number','work_order_date','service_company','car')
    filter = ('maintenance_date',)


class ComplaintsResource(resources.ModelResource):
    class Meta:
        model = Reclamation
        report_skipped = True
        fields = ('id','date_of_failure','operating_hours','failure_node','failure_description','restoration_method','used_spare_parts','restoration_date','downtime_hours','car','service_company')


@admin.register(Reclamation)
class ComplaintsAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = ComplaintsResource
    list_display = ('id','date_of_failure','operating_hours','failure_node','restoration_date','downtime_hours','car','service_company')
    filter = ('date_of_failure',)


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


class UserAdmin(UserAdmin):
    inlines = (UserInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class TechnicResource(resources.ModelResource):
    class Meta:
        model = Technics
        report_skipped = True
        fields = ('id','name','description',)

@admin.register(Technics)
class TechnicAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = TechnicResource
    list_display = ('id','name','description',)
    filter = ('name',)

class EngineResource(resources.ModelResource):
    class Meta:
        model = EngineModels
        report_skipped = True
        fields = ('id','name','description',)

@admin.register(EngineModels)
class EngineAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = EngineResource
    list_display = ('id','name','description',)
    filter = ('name',)

class TransmissionResource(resources.ModelResource):
    class Meta:
        model = TransmissionModels
        report_skipped = True
        fields = ('id','name','description',)

@admin.register(TransmissionModels)
class TransmissionAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = TransmissionResource
    list_display = ('id','name','description',)
    filter = ('name',)

class DrivingBridgeResource(resources.ModelResource):
    class Meta:
        model = DriveAxleType
        report_skipped = True
        fields = ('id','name','description',)

@admin.register(DriveAxleType)
class DrivingBridgeAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = DrivingBridgeResource
    list_display = ('id','name','description',)
    filter = ('name',)

class ControlledBridgeResource(resources.ModelResource):
    class Meta:
        model = SteeringAxleType
        report_skipped = True
        fields = ('id','name','description',)

@admin.register(SteeringAxleType)
class ControlledBridgeAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = ControlledBridgeResource
    list_display = ('id','name','description',)
    filter = ('name',)

class CarResource(resources.ModelResource):
    class Meta:
        model = Car
        report_skipped = True
        fields = (
        'id',
        'factory_number',
        'model',
        'engine_type',
        'engine_id',
        'transmission_type',
        'transmission_id',
        'drive_axle_type',
        'drive_axle_id',
        'steering_axle_type',
        'steering_axle_id',
        'supply_contract_data',
        'shipment_date',
        'сonsignee',
        'consignee_address',
        'car_config',
        'client',
        'service_company',
        )

@admin.register(Car)
class CarAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = CarResource
    list_display = (
        'id',
        'factory_number',
        'model',
        'engine_type',
        'transmission_type',
        'drive_axle_type',
        'steering_axle_type',
        'shipment_date',
        'car_config',
        'client',
        'service_company',
    )
    filter = ('factory_number',)
