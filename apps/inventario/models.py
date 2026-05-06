from django.db import models
from django.core.validators import MinValueValidator
from core.models import ModeloBase


class CategoriaProducto(ModeloBase):
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')

    class Meta:
        db_table = 'categoria_producto'
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'

    def __str__(self):
        return self.nombre


class ProductoBase(ModeloBase):
    """Inventario – Producto genérico. Repuestos y Neumáticos heredan de aquí."""
    class TipoProducto(models.TextChoices):
        REPUESTO = 'REPUESTO', 'Repuesto'
        NEUMATICO = 'NEUMATICO', 'Neumático'
        OTRO = 'OTRO', 'Otro'

    categoria = models.ForeignKey(
        CategoriaProducto, on_delete=models.RESTRICT,
        related_name='productos', verbose_name='Categoría'
    )
    codigo_sku = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='SKU')
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Precio Costo')
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Precio Venta')
    stock_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='Stock Actual')
    stock_minimo = models.IntegerField(default=5, verbose_name='Stock Mínimo')
    tipo_producto = models.CharField(max_length=20, choices=TipoProducto.choices, default=TipoProducto.OTRO, verbose_name='Tipo')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'producto_base'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        indexes = [
            models.Index(fields=['codigo_sku'], name='idx_producto_sku'),
        ]

    @property
    def stock_critico(self):
        return self.stock_actual <= self.stock_minimo

    @property
    def margen_ganancia(self):
        if self.precio_venta > 0:
            return round((self.precio_venta - self.precio_costo) / self.precio_venta * 100, 2)
        return 0

    def __str__(self):
        return f"{self.codigo_sku} – {self.nombre}"


class RepuestoGenerico(ProductoBase):
    """Repuesto con información técnica adicional."""
    marca_repuesto = models.CharField(max_length=50, blank=True, null=True, verbose_name='Marca Repuesto')
    modelo_repuesto = models.CharField(max_length=50, blank=True, null=True, verbose_name='Modelo Repuesto')
    compatibilidad_vehicular = models.TextField(blank=True, null=True, verbose_name='Compatibilidad Vehicular')
    numero_parte = models.CharField(max_length=50, blank=True, null=True, verbose_name='N° de Parte')

    class Meta:
        db_table = 'repuesto_generico'
        verbose_name = 'Repuesto'
        verbose_name_plural = 'Repuestos'
        indexes = [
            models.Index(fields=['marca_repuesto'], name='idx_repuesto_marca'),
        ]

    def save(self, *args, **kwargs):
        self.tipo_producto = ProductoBase.TipoProducto.REPUESTO
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marca_repuesto} {self.modelo_repuesto} – {self.nombre}"


class Neumatico(ProductoBase):
    """Neumático con especificaciones técnicas."""
    class TipoNeumatico(models.TextChoices):
        VERANO = 'VERANO', 'Verano'
        INVIERNO = 'INVIERNO', 'Invierno'
        ALL_SEASON = 'ALL_SEASON', 'All Season'

    ancho = models.IntegerField(verbose_name='Ancho (mm)')
    perfil = models.IntegerField(verbose_name='Perfil')
    diametro_rin = models.IntegerField(verbose_name='Diámetro Rin')
    indice_carga = models.CharField(max_length=5, blank=True, null=True, verbose_name='Índice de Carga')
    indice_velocidad = models.CharField(max_length=5, blank=True, null=True, verbose_name='Índice de Velocidad')
    tipo_neumatico = models.CharField(max_length=20, choices=TipoNeumatico.choices, blank=True, null=True, verbose_name='Tipo')
    marca_neumatico = models.CharField(max_length=30, verbose_name='Marca')
    modelo_neumatico = models.CharField(max_length=50, blank=True, null=True, verbose_name='Modelo')

    class Meta:
        db_table = 'neumatico'
        verbose_name = 'Neumático'
        verbose_name_plural = 'Neumáticos'
        indexes = [
            models.Index(fields=['ancho', 'perfil', 'diametro_rin'], name='idx_neumatico_medida'),
        ]

    @property
    def medida_completa(self):
        return f"{self.ancho}/{self.perfil}R{self.diametro_rin}"

    def save(self, *args, **kwargs):
        self.tipo_producto = ProductoBase.TipoProducto.NEUMATICO
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marca_neumatico} {self.medida_completa}"


class MovimientoStock(ModeloBase):
    """Registro de entradas y salidas de inventario."""
    class TipoMovimiento(models.TextChoices):
        ENTRADA = 'ENTRADA', 'Entrada'
        SALIDA = 'SALIDA', 'Salida'
        AJUSTE = 'AJUSTE', 'Ajuste'

    producto = models.ForeignKey(ProductoBase, on_delete=models.CASCADE, related_name='movimientos', verbose_name='Producto')
    orden = models.ForeignKey('ordenes.OrdenTrabajo', on_delete=models.SET_NULL, blank=True, null=True, related_name='movimientos_stock', verbose_name='Orden')
    tipo_movimiento = models.CharField(max_length=10, choices=TipoMovimiento.choices, verbose_name='Tipo')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad')
    stock_resultante = models.IntegerField(verbose_name='Stock Resultante')
    motivo = models.CharField(max_length=200, verbose_name='Motivo')
    usuario = models.ForeignKey('accounts.Usuario', on_delete=models.SET_NULL, blank=True, null=True, related_name='movimientos_stock', verbose_name='Usuario')

    class Meta:
        db_table = 'movimiento_stock'
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'
        indexes = [
            models.Index(fields=['producto'], name='idx_movimiento_producto'),
            models.Index(fields=['fecha_creacion'], name='idx_movimiento_fecha'),
        ]

    def __str__(self):
        return f"{self.get_tipo_movimiento_display()} – {self.producto.nombre} ({self.cantidad})"
