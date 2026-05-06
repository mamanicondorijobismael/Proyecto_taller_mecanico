from django.contrib import admin
from .models import ProductoBase, RepuestoGenerico, Neumatico, CategoriaProducto, MovimientoStock

@admin.register(CategoriaProducto)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(ProductoBase)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_sku', 'nombre', 'tipo_producto', 'precio_costo', 'precio_venta', 'stock_actual', 'stock_minimo', 'stock_critico', 'activo')
    list_filter = ('tipo_producto', 'activo', 'categoria')
    search_fields = ('codigo_sku', 'nombre')
    ordering = ('nombre',)

@admin.register(RepuestoGenerico)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('codigo_sku', 'nombre', 'marca_repuesto', 'modelo_repuesto', 'stock_actual', 'activo')
    search_fields = ('codigo_sku', 'nombre', 'marca_repuesto', 'compatibilidad_vehicular')

@admin.register(Neumatico)
class NeumaticoAdmin(admin.ModelAdmin):
    list_display = ('codigo_sku', 'marca_neumatico', 'medida_completa', 'tipo_neumatico', 'stock_actual', 'activo')
    search_fields = ('codigo_sku', 'marca_neumatico', 'modelo_neumatico')
    list_filter = ('tipo_neumatico', 'marca_neumatico')

@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo_movimiento', 'cantidad', 'stock_resultante', 'motivo', 'fecha_creacion')
    list_filter = ('tipo_movimiento',)
    readonly_fields = ('fecha_creacion',)
