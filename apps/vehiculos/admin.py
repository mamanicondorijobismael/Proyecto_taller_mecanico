from django.contrib import admin
from .models import Vehiculo

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'anio', 'cliente', 'kilometraje_actual')
    list_filter = ('marca',)
    search_fields = ('patente', 'marca', 'modelo', 'vin', 'cliente__nombre_razon_social')
    ordering = ('patente',)
