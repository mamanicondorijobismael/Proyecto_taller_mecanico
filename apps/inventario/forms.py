from django import forms
from .models import RepuestoGenerico, Neumatico

class RepuestoForm(forms.ModelForm):
    class Meta:
        model = RepuestoGenerico
        fields = ['categoria', 'codigo_sku', 'nombre', 'descripcion', 'precio_costo', 'precio_venta', 'stock_actual', 'stock_minimo', 'marca_repuesto', 'modelo_repuesto', 'numero_parte']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'codigo_sku': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm uppercase'}),
            'nombre': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm', 'rows': 2}),
            'precio_costo': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'marca_repuesto': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'modelo_repuesto': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'numero_parte': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm uppercase'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import CategoriaProducto
        # Filtrar categorías para que no aparezcan las de neumáticos
        self.fields['categoria'].queryset = CategoriaProducto.objects.exclude(nombre__icontains='Neumático').exclude(nombre__icontains='Cubierta')

class NeumaticoForm(forms.ModelForm):
    class Meta:
        model = Neumatico
        fields = ['categoria', 'codigo_sku', 'nombre', 'descripcion', 'precio_costo', 'precio_venta', 'stock_actual', 'stock_minimo', 'ancho', 'perfil', 'diametro_rin', 'indice_carga', 'indice_velocidad', 'tipo_neumatico', 'marca_neumatico', 'modelo_neumatico']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'codigo_sku': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm uppercase'}),
            'nombre': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm', 'rows': 2}),
            'precio_costo': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'perfil': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'diametro_rin': forms.NumberInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'indice_carga': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'indice_velocidad': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm uppercase'}),
            'tipo_neumatico': forms.Select(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'marca_neumatico': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
            'modelo_neumatico': forms.TextInput(attrs={'class': 'form-input w-full px-3 py-2 border border-outline-variant rounded-xl text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import CategoriaProducto
        # Filtrar categorías para que solo aparezcan las de neumáticos
        self.fields['categoria'].queryset = CategoriaProducto.objects.filter(models.Q(nombre__icontains='Neumático') | models.Q(nombre__icontains='Cubierta'))
        
        # Intentar preseleccionar una categoría válida si es nuevo
        if not self.instance.pk:
            cat = self.fields['categoria'].queryset.first()
            if cat:
                self.initial['categoria'] = cat.pk
