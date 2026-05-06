from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.ordenes.models import OrdenTrabajo
from apps.facturas.models import Factura

def es_admin_o_dueno(user):
    return user.is_superuser or user.rol in ['DUENO', 'ADMINISTRADOR']

@login_required
@user_passes_test(es_admin_o_dueno)
def reportes_dashboard(request):
    hoy = timezone.now()
    inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Simple chart data (last 6 months)
    meses_labels = []
    ingresos_data = []
    
    for i in range(5, -1, -1):
        d = hoy - timedelta(days=30*i)
        meses_labels.append(d.strftime("%b %Y"))
        # Dummy data for chart if actual queries are too complex for initial setup
        ingresos_data.append(0) 

    # For current month:
    ordenes_mes = OrdenTrabajo.objects.filter(fecha_creacion__gte=inicio_mes, estado__in=['COMPLETADA', 'FACTURADA'])
    ingresos_totales = ordenes_mes.aggregate(total=Sum('total'))['total'] or 0
    
    facturas_pendientes = Factura.objects.filter(estado_pago__in=['PENDIENTE', 'PARCIAL'])
    saldo_por_cobrar = facturas_pendientes.aggregate(total=Sum('saldo_pendiente'))['total'] or 0

    context = {
        'ingresos_totales': ingresos_totales,
        'saldo_por_cobrar': saldo_por_cobrar,
        'ordenes_mes_count': ordenes_mes.count(),
        'meses_labels': meses_labels,
        'ingresos_data': ingresos_data,
    }
    return render(request, 'reportes/dashboard.html', context)

from apps.inventario.models import ProductoBase, MovimientoStock
from apps.ordenes.models import DetalleProducto

@login_required
@user_passes_test(es_admin_o_dueno)
def reporte_inventario(request):
    # Productos más vendidos
    mas_vendidos = DetalleProducto.objects.values('producto__nombre', 'producto__codigo_sku')\
        .annotate(total_cantidad=Sum('cantidad'))\
        .order_by('-total_cantidad')[:10]
        
    # Últimos movimientos de stock
    movimientos = MovimientoStock.objects.all().order_by('-fecha')[:20]
    
    # Resumen de stock por categoría
    resumen_stock = ProductoBase.objects.values('categoria__nombre')\
        .annotate(total_stock=Sum('stock_actual'))\
        .order_by('-total_stock')
        
    context = {
        'mas_vendidos': mas_vendidos,
        'movimientos': movimientos,
        'resumen_stock': resumen_stock,
    }
    return render(request, 'reportes/inventario.html', context)

@login_required
@user_passes_test(es_admin_o_dueno)
def reporte_producto(request, pk):
    producto = get_object_or_404(ProductoBase, pk=pk)
    movimientos = MovimientoStock.objects.filter(producto=producto).order_by('-fecha')
    
    # Ventas en órdenes
    ventas = DetalleProducto.objects.filter(producto=producto).select_related('orden', 'orden__vehiculo')
    
    context = {
        'producto': producto,
        'movimientos': movimientos,
        'ventas': ventas,
    }
    return render(request, 'reportes/producto_detalle.html', context)
