from django.db import models
from django.core.validators import MinValueValidator
from core.models import ModeloBase
from apps.ordenes.models import OrdenTrabajo
from apps.clientes.models import Cliente


class Factura(ModeloBase):
    """Factura generada desde una orden completada."""
    class EstadoPago(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PARCIAL = 'PARCIAL', 'Pago Parcial'
        PAGADA = 'PAGADA', 'Pagada'

    numero_factura = models.CharField(max_length=20, unique=True, verbose_name='N° Factura')
    orden = models.OneToOneField(OrdenTrabajo, on_delete=models.RESTRICT, related_name='factura', verbose_name='Orden de Trabajo')
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name='facturas', verbose_name='Cliente')
    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Emisión')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Subtotal')
    iva = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='IVA')
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total')
    estado_pago = models.CharField(max_length=20, choices=EstadoPago.choices, default=EstadoPago.PENDIENTE, db_index=True, verbose_name='Estado de Pago')
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Saldo Pendiente')

    class Meta:
        db_table = 'factura'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        indexes = [
            models.Index(fields=['cliente'], name='idx_factura_cliente'),
            models.Index(fields=['estado_pago'], name='idx_factura_estado'),
        ]

    def __str__(self):
        return f"Factura {self.numero_factura} – {self.cliente}"


class Pago(ModeloBase):
    """Pago total o parcial de una factura."""
    class MetodoPago(models.TextChoices):
        EFECTIVO = 'EFECTIVO', 'Efectivo'
        TARJETA = 'TARJETA', 'Tarjeta'
        TRANSFERENCIA = 'TRANSFERENCIA', 'Transferencia'
        CHEQUE = 'CHEQUE', 'Cheque'

    factura = models.ForeignKey(Factura, on_delete=models.RESTRICT, related_name='pagos', verbose_name='Factura')
    monto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='Monto')
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices, verbose_name='Método de Pago')
    referencia = models.CharField(max_length=100, blank=True, null=True, verbose_name='Referencia')
    usuario = models.ForeignKey('accounts.Usuario', on_delete=models.RESTRICT, related_name='pagos_registrados', verbose_name='Registrado por')

    class Meta:
        db_table = 'pago'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        indexes = [
            models.Index(fields=['factura'], name='idx_pago_factura'),
        ]

    def __str__(self):
        return f"Pago ${self.monto} – Factura {self.factura.numero_factura}"
