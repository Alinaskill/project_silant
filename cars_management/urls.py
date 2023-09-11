from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', CarSearchView.as_view(), name='car_search_list'),

    path('cars/', CarListView.as_view(), name='car_list'),
    path('car/<pk>/detail', CarDetailView.as_view(), name='car_detail'),
    path('car/create', CarCreateView.as_view(), name='car_create'),
    path('car/<pk>/update', CarUpdateView.as_view(), name='car_update'),
    path('car/<pk>/delete', CarDeleteView.as_view(), name='car_delete'),
    path('car/<pk>/description/<attribute>', CarDescriptionView.as_view(), name='car_description'),

    path('maintenances/', MaintenanceListView.as_view(), name='maintenance_list'),
    path('maintenance/create', MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('maintenance/<pk>/update', MaintenanceUpdateView.as_view(), name='maintenance_update'),
    path('maintenance/<pk>/delete', MaintenanceDeleteView.as_view(), name='maintenance_delete'),
    path('car/<pk>/maintenances', MaintenanceCarListView.as_view(), name='car_maintenance'),
    path('maintenance/<pk>/description/<attribute>', MaintenanceDescriptionView.as_view(),
         name='maintenance_description'),

    path('complaints/', ComplaintListView.as_view(), name='complaint_list'),
    path('complaint/create', ComplaintCreateView.as_view(), name='complaint_create'),
    path('complaint/<pk>/update', ComplaintUpdateView.as_view(), name='complaint_update'),
    path('complaint/<pk>/delete', ComplaintDeleteView.as_view(), name='complaint_delete'),
    path('car/<pk>/complaints', ComplaintCarListView.as_view(), name='car_complaint'),
    path('complaint/<pk>/description/<attribute>', ComplaintDescriptionView.as_view(), name='complaint_description'),
]
