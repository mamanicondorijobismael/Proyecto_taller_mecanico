from django.contrib import admin
from .models import Factura, Pago


class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1
    fields = ('monto', 'metodo_pago', 'referencia', 'usuario')


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'cliente', 'total', 'estado_pago', 'saldo_pendiente', 'fecha_emision')
    list_filter = ('estado_pago',)
    search_fields = ('numero_factura', 'cliente__nombre_razon_social')
    readonly_fields = ('numero_factura', 'fecha_emision', 'subtotal', 'iva', 'total')
    inlines = [PagoInline]

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('factura', 'monto', 'metodo_pago', 'fecha_creacion', 'usuario')
    list_filter = ('metodo_pago',)
    readonly_fields = ('fecha_creacion',)
