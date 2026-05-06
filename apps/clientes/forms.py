from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_razon_social', 'documento', 'telefono', 'email', 'direccion', 'activo']
        widgets = {
            'nombre_razon_social': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'documento': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'telefono': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'direccion': forms.Textarea(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'rounded border-outline-variant text-primary focus:ring-primary w-4 h-4'}),
        }
