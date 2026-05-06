from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'patente', 'marca', 'modelo', 'anio', 'vin', 'kilometraje_actual', 'color']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'patente': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary uppercase'}),
            'marca': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'modelo': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'anio': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'vin': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'kilometraje_actual': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'color': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
        }
