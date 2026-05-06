from django.db import models
from django.core.validators import MinValueValidator
from core.models import ModeloBase
from apps.vehiculos.models import Vehiculo
from apps.inventario.models import ProductoBase


class OrdenTrabajo(ModeloBase):
    """Orden de trabajo del taller."""
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_PROCESO = 'EN_PROCESO', 'En Proceso'
        PAUSADA = 'PAUSADA', 'Pausada'
        COMPLETADA = 'COMPLETADA', 'Completada'
        FACTURADA = 'FACTURADA', 'Facturada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    numero_orden = models.CharField(max_length=20, unique=True, verbose_name='N° Orden')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.RESTRICT, related_name='ordenes', verbose_name='Vehículo')
    usuario_creador = models.ForeignKey('accounts.Usuario', on_delete=models.RESTRICT, related_name='ordenes_creadas', verbose_name='Creado por')
    fecha_cierre = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Cierre')
    kilometraje = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Kilometraje')
    diagnostico = models.TextField(blank=True, null=True, verbose_name='Diagnóstico')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE, db_index=True, verbose_name='Estado')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Subtotal')
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='IVA')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total')

    class Meta:
        db_table = 'orden_trabajo'
        verbose_name = 'Orden de Trabajo'
        verbose_name_plural = 'Órdenes de Trabajo'
        indexes = [
            models.Index(fields=['vehiculo'], name='idx_orden_vehiculo'),
            models.Index(fields=['estado'], name='idx_orden_estado'),
            models.Index(fields=['fecha_creacion'], name='idx_orden_fecha'),
        ]

    def __str__(self):
        return f"OT #{self.numero_orden} – {self.vehiculo.patente}"

    def actualizar_totales(self):
        from django.conf import settings
        from decimal import Decimal
        
        iva_porcentaje = getattr(settings, 'IVA_PORCENTAJE', 21)
        
        subtotal_servicios = sum(s.subtotal for s in self.servicios.all())
        subtotal_productos = sum(p.subtotal for p in self.productos.all())
        
        self.subtotal = subtotal_servicios + subtotal_productos
        self.iva = self.subtotal * (Decimal(iva_porcentaje) / Decimal(100))
        self.total = self.subtotal + self.iva
        self.save()


class DetalleServicio(ModeloBase):
    """Servicio aplicado en una orden de trabajo."""
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='servicios', verbose_name='Orden')
    descripcion = models.CharField(max_length=200, verbose_name='Descripción')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1, validators=[MinValueValidator(0)], verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio Unitario')

    class Meta:
        db_table = 'detalle_servicio'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.descripcion} × {self.cantidad}"


class DetalleProducto(ModeloBase):
    """Producto utilizado en una orden de trabajo."""
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name='productos', verbose_name='Orden')
    producto = models.ForeignKey(ProductoBase, on_delete=models.RESTRICT, related_name='usos', verbose_name='Producto')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='Cantidad')
    precio_unitario_aplicado = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio Unitario')

    class Meta:
        db_table = 'detalle_producto'
        verbose_name = 'Producto en Orden'
        verbose_name_plural = 'Productos en Orden'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario_aplicado

    def __str__(self):
        return f"{self.producto.nombre} × {self.cantidad}"
