from django.db import models
from core.models import ModeloBase
from apps.vehiculos.models import Vehiculo


class TipoServicio(ModeloBase):
    """Tipos de servicio disponibles en el taller."""
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    precio_base = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Precio Base')

    class Meta:
        db_table = 'tipo_servicio'
        verbose_name = 'Tipo de Servicio'
        verbose_name_plural = 'Tipos de Servicios'

    def __str__(self):
        return self.nombre


class IntervaloMantenimiento(ModeloBase):
    """Intervalo de mantenimiento por tipo de servicio."""
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE, related_name='intervalos', verbose_name='Tipo de Servicio')
    intervalo_kilometros = models.IntegerField(blank=True, null=True, verbose_name='Intervalo (km)')
    intervalo_meses = models.IntegerField(blank=True, null=True, verbose_name='Intervalo (meses)')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'intervalo_mantenimiento'
        verbose_name = 'Intervalo de Mantenimiento'
        verbose_name_plural = 'Intervalos de Mantenimiento'

    def __str__(self):
        return f"{self.tipo_servicio.nombre} – c/{self.intervalo_kilometros or self.intervalo_meses}"


class AlertaMantenimiento(ModeloBase):
    """Alerta generada para mantenimiento preventivo pendiente."""
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        NOTIFICADA = 'NOTIFICADA', 'Notificada'
        COMPLETADA = 'COMPLETADA', 'Completada'
        IGNORADA = 'IGNORADA', 'Ignorada'

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='alertas', verbose_name='Vehículo')
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.RESTRICT, related_name='alertas', verbose_name='Tipo de Servicio')
    kilometraje_estimado = models.IntegerField(blank=True, null=True, verbose_name='Kilometraje Estimado')
    fecha_estimada = models.DateField(blank=True, null=True, verbose_name='Fecha Estimada')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE, db_index=True, verbose_name='Estado')
    fecha_notificacion = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Notificación')

    class Meta:
        db_table = 'alerta_mantenimiento'
        verbose_name = 'Alerta de Mantenimiento'
        verbose_name_plural = 'Alertas de Mantenimiento'
        indexes = [
            models.Index(fields=['vehiculo'], name='idx_alerta_vehiculo'),
            models.Index(fields=['estado'], name='idx_alerta_estado'),
        ]

    def __str__(self):
        return f"Alerta {self.vehiculo.patente} – {self.tipo_servicio.nombre}"
