from django.contrib import admin
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'vehiculo', 'fecha_hora', 'servicio_solicitado', 'estado')
    list_filter = ('estado',)
    search_fields = ('cliente__nombre_razon_social', 'vehiculo__patente', 'servicio_solicitado')
    ordering = ('-fecha_hora',)
