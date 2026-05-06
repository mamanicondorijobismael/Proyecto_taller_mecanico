from django.db import models
from django.core.validators import RegexValidator
from core.models import ModeloBase


class Cliente(ModeloBase):
    """Clientes del taller mecánico."""
    nombre_razon_social = models.CharField(max_length=100, verbose_name='Nombre / Razón Social')
    documento = models.CharField(
        max_length=20, unique=True, db_index=True,
        validators=[RegexValidator(r'^\d{7,11}$', 'Documento: 7 a 11 dígitos')],
        verbose_name='Documento (DNI/CUIT)'
    )
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True, verbose_name='Email')
    direccion = models.TextField(blank=True, null=True, verbose_name='Dirección')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        indexes = [
            models.Index(fields=['nombre_razon_social'], name='idx_cliente_nombre'),
        ]

    def __str__(self):
        return f"{self.nombre_razon_social} ({self.documento})"
