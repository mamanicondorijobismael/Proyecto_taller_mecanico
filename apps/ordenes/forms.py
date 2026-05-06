from django import forms
from .models import OrdenTrabajo, DetalleServicio, DetalleProducto

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['numero_orden', 'vehiculo', 'kilometraje', 'diagnostico', 'observaciones', 'estado']
        widgets = {
            'numero_orden': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'vehiculo': forms.Select(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary', 'rows': 2}),
            'estado': forms.Select(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
        }

class DetalleServicioForm(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ['descripcion', 'cantidad', 'precio_unitario']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
        }

class DetalleProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleProducto
        fields = ['producto', 'cantidad', 'precio_unitario_aplicado']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'precio_unitario_aplicado': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
        }
