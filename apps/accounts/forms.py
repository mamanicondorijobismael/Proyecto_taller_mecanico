from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class UsuarioCustomCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre_completo', 'rol', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'rol': forms.Select(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-outline-variant text-primary focus:ring-primary w-4 h-4'}),
        }

class UsuarioCustomChangeForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre_completo', 'rol', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'rol': forms.Select(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm bg-surface-bright focus:outline-none focus:border-primary'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-outline-variant text-primary focus:ring-primary w-4 h-4'}),
        }
