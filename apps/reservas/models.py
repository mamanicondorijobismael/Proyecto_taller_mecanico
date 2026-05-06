from django.db import models
from core.models import ModeloBase
from apps.clientes.models import Cliente
from apps.vehiculos.models import Vehiculo


class Reserva(ModeloBase):
    """Cita programada para un servicio."""
    class Estado(models.TextChoices):
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        CANCELADA = 'CANCELADA', 'Cancelada'
        COMPLETADA = 'COMPLETADA', 'Completada'

    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name='reservas', verbose_name='Cliente')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.RESTRICT, related_name='reservas', verbose_name='Vehículo')
    fecha_hora = models.DateTimeField(verbose_name='Fecha y Hora')
    servicio_solicitado = models.CharField(max_length=200, verbose_name='Servicio Solicitado')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.CONFIRMADA, db_index=True, verbose_name='Estado')
    notas = models.TextField(blank=True, null=True, verbose_name='Notas')
    orden_generada = models.ForeignKey(
        'ordenes.OrdenTrabajo', on_delete=models.SET_NULL,
        blank=True, null=True, related_name='reserva_origen', verbose_name='Orden Generada'
    )

    class Meta:
        db_table = 'reserva'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        indexes = [
            models.Index(fields=['fecha_hora'], name='idx_reserva_fecha'),
            models.Index(fields=['estado'], name='idx_reserva_estado'),
        ]

    def __str__(self):
        return f"Reserva {self.cliente} – {self.fecha_hora:%d/%m/%Y %H:%M}"
