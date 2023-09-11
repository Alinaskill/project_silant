from django import forms
from .models import *


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'
        widgets ={
            'maintenance_type': forms.RadioSelect()
        }


class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = '__all__'


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'