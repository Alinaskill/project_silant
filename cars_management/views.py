from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CarSerializer, ServiceSerializer, ClaimSerializer
from .forms import *
from django.contrib.auth.models import User


def create_groups(sender, **kwargs):
    if not Group.objects.create(name='Клиент'):
        Group.objects.create(name='Клиент')

    if not Group.objects.create(name='Сервисная организация'):
        Group.objects.create(name='Сервисная организация')

    if not Group.objects.create(name='Менеджер'):
        Group.objects.create(name='Менеджер')

def is_client(user):
    return user.groups.filter(name='Клиент').exists()

def is_service_organization(user):
    return user.groups.filter(name='Сервисная организация').exists()

def is_manager(user):
    return user.groups.filter(name='Менеджер').exists()


@api_view(['GET'])
@login_required
@user_passes_test(is_client)
def car_list(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@login_required
@user_passes_test(is_client)
def car_detail(request):
    factory_number = request.GET.get('factory_number')
    try:
        car = Car.objects.get(factory_number=factory_number)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    except Car.DoesNotExist:
        message = "Данных о машине с таким заводским номером нет в системе."
        return Response({'message': message})


@api_view(['GET'])
@login_required
@user_passes_test(is_service_organization)
def service_list(request, id):
    try:
        car = Car.objects.get(id=id)
        services = Maintenance.objects.filter(car=car)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    except Car.DoesNotExist:
        message = "Данных о машине с таким идентификатором нет в системе."
        return Response({'message': message})


@api_view(['GET'])
@login_required
@user_passes_test(is_manager)
def claim_list(request, id):
    try:
        car = Car.objects.get(id=id)
        claims = Reclamation.objects.filter(car=car)
        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)
    except Car.DoesNotExist:
        message = "Данных о машине с таким идентификатором нет в системе."
        return Response({'message': message})


def login(request):
    # ToDo: Put actual template here
    return render(request, 'login.html')


class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('car_list')
        else:
            return redirect('car_search_list')


class CarSearchView(ListView):
    model = Car
    template_name = 'cars_management/car_search.html'
    queryset = Car.objects.all()


class CarListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'cars_management/car_list.html'

    def get_queryset(self):
        if not self.request.user.is_staff:
            user = User.objects.get(pk = self.request.user.pk)
            try:
                profile = UserProfile.objects.get(user = user)
                if profile.is_service:
                    return Car.objects.filter(service_company = profile.service_company)
            except:
                return Car.objects.filter(client = user)
        else:
            return Car.objects.all()


class CarDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'cars_management.view_car'
    model = Car
    template_name = 'cars_management/car_view.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CarCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'cars_management.add_car'
    model = Car
    form_class = CarForm
    template_name = 'cars_management/car_create.html'
    success_url = reverse_lazy('car_list')


class CarUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'cars_management.change_car'
    model = Car
    form_class = CarForm
    template_name = 'cars_management/car_update.html'
    success_url = reverse_lazy('car_list')


class CarDescriptionView(TemplateView):
    template_name = 'cars_management/modal_description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = Car.objects.get(pk = self.kwargs["pk"])
        attribute = context['attribute']
        if attribute == 'technic':
            context['attribute'] = car.model.name
            context['description'] = car.model.description
        elif attribute == 'engine':
            context['attribute'] = car.engine_type.name
            context['description'] = car.engine_type.description
        elif attribute == 'transmission':
            context['attribute'] = car.transmission_type.name
            context['description'] = car.transmission_type.description
        elif attribute == 'driving_bridge':
            context['attribute'] = car.drive_axle_type.name
            context['description'] = car.drive_axle_type.description
        elif attribute == 'controlled_bridge':
            context['attribute'] = car.steering_axle_type.name
            context['description'] = car.steering_axle_type.description
        elif attribute == 'car_config':
            context['attribute'] = 'Комплектация'
            context['description'] = car.car_config
        elif attribute == 'service_company':
            context['attribute'] = car.service_company
            context['description'] = car.service_company.description
        return context


class CarDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'cars_management.delete_car'
    model = Car
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('car_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'car'
        return context


class MaintenanceListView(LoginRequiredMixin, PermissionRequiredMixin,  ListView):
    permission_required = 'cars_management.view_maintenance'
    model = Maintenance
    template_name = 'cars_management/maintenance_list.html'

    def get_queryset(self):
        if not self.request.user.is_staff:
            user = User.objects.get(pk = self.request.user.pk)
            try:
                profile = UserProfile.objects.get(user = user)
                if profile.is_service:
                    return Maintenance.objects.filter(service_company = profile.service_company)
            except:
                return Maintenance.objects.filter(car__client = user)
        else:
            return Maintenance.objects.all()


class MaintenanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'cars_management.add_maintenance'
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'cars_management/maintenance_create.html'
    success_url = reverse_lazy('maintenance_list')


class MaintenanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'cars_management.change_maintenance'
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'cars_management/maintenance_update.html'
    success_url = reverse_lazy('maintenance_list')


class MaintenanceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'cars_management.delete_maintenance'
    model = Maintenance
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('maintenance_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'maintenance'
        return context


class ComplaintListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cars_management.view_reclamation'
    model = Reclamation
    template_name = 'cars_management/complaint_list.html'

    def get_queryset(self):
        if not self.request.user.is_staff:
            user = User.objects.get(pk = self.request.user.pk)
            try:
                profile = UserProfile.objects.get(user = user)
                if profile.is_service:
                    return Reclamation.objects.filter(service_company = profile.service_company)
            except:
                return Reclamation.objects.filter(car__client = user)
        else:
            return Reclamation.objects.all()


class ComplaintCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'cars_management.add_reclamation'
    model = Reclamation
    form_class = ReclamationForm
    template_name = 'cars_management/complaint_create.html'
    success_url = reverse_lazy('complaint_list')


class ComplaintUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'cars_management.change_reclamation'
    model = Reclamation
    form_class = ReclamationForm
    template_name = 'cars_management/complaint_update.html'
    success_url = reverse_lazy('complaint_list')


class ComplaintDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'cars_management.delete_reclamation'
    model = Reclamation
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('complaint_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'сomplaint'
        return context


class MaintenanceCarListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cars_management.view_maintenance'
    model = Maintenance
    template_name = 'cars_management/maintenance_car.html'

    def get_queryset(self):
        car = Car.objects.get(pk = self.kwargs["pk"])
        return Maintenance.objects.filter(car = car)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["car"] = Car.objects.get(pk = self.kwargs["pk"])
        return context


class ComplaintCarListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cars_management.view_reclamation'
    model = Reclamation
    template_name = 'cars_management/complaint_car.html'

    def get_queryset(self):
        car = Car.objects.get(pk = self.kwargs["pk"])
        return Reclamation.objects.filter(car = car)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["car"] = Car.objects.get(pk = self.kwargs["pk"])
        return context


class MaintenanceDescriptionView(TemplateView):
    template_name= 'cars_management/modal_description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maintenance = Maintenance.objects.get(pk = self.kwargs["pk"])
        attribute = context['attribute']
        if attribute == 'type':
            context['attribute'] = maintenance.maintenance_type.name
            context['description'] = maintenance.maintenance_type.description
        elif attribute == 'service_company':
            context['attribute'] = maintenance.service_company.name
            context['description'] = maintenance.service_company.description
        return context


class ComplaintDescriptionView(TemplateView):
    template_name= 'cars_management/modal_description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        complaint = Reclamation.objects.get(pk = self.kwargs["pk"])
        attribute = context['attribute']
        if attribute == 'node_failure':
            context['attribute'] = complaint.failure_node.name
            context['description'] = complaint.failure_node.description
        elif attribute == 'method_recovery':
            context['attribute'] = complaint.restoration_method.name
            context['description'] = complaint.restoration_method.description
        elif attribute == 'service_company':
            context['attribute'] = complaint.service_company.name
            context['description'] = complaint.service_company.description
        return context