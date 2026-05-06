from django.db import models
from django.utils import timezone


class ModeloBase(models.Model):
    """
    Modelo abstracto base: todos los modelos heredan fechas de creación y modificación.
    """
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name='Fecha de Creación'
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Modificación'
    )

    class Meta:
        abstract = True
        ordering = ['-fecha_creacion']


class Auditoria(models.Model):
    """
    Registro de auditoría para cambios críticos en el sistema.
    """
    class Operacion(models.TextChoices):
        INSERT = 'INSERT', 'Inserción'
        UPDATE = 'UPDATE', 'Actualización'
        DELETE = 'DELETE', 'Eliminación'

    tabla_afectada = models.CharField(max_length=50, verbose_name='Tabla Afectada')
    id_registro = models.BigIntegerField(verbose_name='ID del Registro')
    operacion = models.CharField(max_length=10, choices=Operacion.choices, verbose_name='Operación')
    valores_anteriores = models.JSONField(blank=True, null=True, verbose_name='Valores Anteriores')
    valores_nuevos = models.JSONField(blank=True, null=True, verbose_name='Valores Nuevos')
    id_usuario = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='auditorias',
        verbose_name='Usuario'
    )
    fecha_operacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Operación')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='Dirección IP')

    class Meta:
        db_table = 'auditoria'
        verbose_name = 'Auditoría'
        verbose_name_plural = 'Auditorías'
        ordering = ['-fecha_operacion']
        indexes = [
            models.Index(fields=['tabla_afectada'], name='idx_auditoria_tabla'),
            models.Index(fields=['fecha_operacion'], name='idx_auditoria_fecha'),
        ]

    def __str__(self):
        return f"{self.operacion} en {self.tabla_afectada} ({self.fecha_operacion:%Y-%m-%d %H:%M})"
