from django.db import models
from django.core.validators import MinValueValidator
from core.models import ModeloBase
from apps.clientes.models import Cliente


class Vehiculo(ModeloBase):
    """Vehículo asociado a un cliente."""
    cliente = models.ForeignKey(
        Cliente, on_delete=models.RESTRICT,
        related_name='vehiculos', verbose_name='Propietario'
    )
    patente = models.CharField(max_length=10, unique=True, db_index=True, verbose_name='Patente')
    marca = models.CharField(max_length=30, verbose_name='Marca')
    modelo = models.CharField(max_length=50, verbose_name='Modelo')
    anio = models.IntegerField(blank=True, null=True, verbose_name='Año')
    vin = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='VIN / Chasis')
    kilometraje_actual = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Kilometraje Actual'
    )
    color = models.CharField(max_length=30, blank=True, null=True, verbose_name='Color')

    class Meta:
        db_table = 'vehiculo'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        indexes = [
            models.Index(fields=['cliente'], name='idx_vehiculo_cliente'),
        ]

    def __str__(self):
        return f"{self.patente} – {self.marca} {self.modelo}"
