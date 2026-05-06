from django.contrib import admin
from .models import OrdenTrabajo, DetalleServicio, DetalleProducto


class DetalleServicioInline(admin.TabularInline):
    model = DetalleServicio
    extra = 1
    fields = ('descripcion', 'cantidad', 'precio_unitario')


class DetalleProductoInline(admin.TabularInline):
    model = DetalleProducto
    extra = 1
    fields = ('producto', 'cantidad', 'precio_unitario_aplicado')


@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'vehiculo', 'estado', 'subtotal', 'iva', 'total', 'fecha_creacion')
    list_filter = ('estado',)
    search_fields = ('numero_orden', 'vehiculo__patente', 'vehiculo__cliente__nombre_razon_social')
    readonly_fields = ('numero_orden', 'fecha_creacion', 'fecha_modificacion', 'subtotal', 'iva', 'total')
    inlines = [DetalleServicioInline, DetalleProductoInline]
    ordering = ('-fecha_creacion',)
