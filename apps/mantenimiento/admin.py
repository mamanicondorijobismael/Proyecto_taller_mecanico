from django.contrib import admin
from .models import TipoServicio, IntervaloMantenimiento, AlertaMantenimiento


@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_base', 'fecha_creacion')
    search_fields = ('nombre',)


@admin.register(IntervaloMantenimiento)
class IntervaloAdmin(admin.ModelAdmin):
    list_display = ('tipo_servicio', 'intervalo_kilometros', 'intervalo_meses', 'activo')
    list_filter = ('activo', 'tipo_servicio')


@admin.register(AlertaMantenimiento)
class AlertaMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'tipo_servicio', 'estado', 'kilometraje_estimado', 'fecha_estimada')
    list_filter = ('estado',)
    search_fields = ('vehiculo__patente', 'tipo_servicio__nombre')
