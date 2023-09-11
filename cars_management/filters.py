import django_filters
from .models import Car, Maintenance, Reclamation


class MachineFilter(django_filters.FilterSet):
    model = django_filters.CharFilter(lookup_expr='icontains')
    engine_model = django_filters.CharFilter(lookup_expr='icontains')
    transmission_model = django_filters.CharFilter(lookup_expr='icontains')
    controlled_axle_model = django_filters.CharFilter(lookup_expr='icontains')
    driving_axle_model = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Car
        fields = ['model', 'engine_model', 'transmission_model', 'controlled_axle_model', 'driving_axle_model']


class MaintenanceFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(lookup_expr='icontains')
    machine_serial_number = django_filters.CharFilter(lookup_expr='icontains')
    service_company = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Maintenance
        fields = ['type', 'machine_serial_number', 'service_company']


class ReclamationFilter(django_filters.FilterSet):
    failure_node = django_filters.CharFilter(lookup_expr='icontains')
    restoration_method = django_filters.CharFilter(lookup_expr='icontains')
    service_company = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Reclamation
        fields = ['failure_node', 'restoration_method', 'service_company']