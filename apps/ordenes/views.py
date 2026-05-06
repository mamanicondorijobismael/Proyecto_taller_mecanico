from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrdenTrabajo
from .forms import OrdenTrabajoForm
from apps.accounts.decorators import es_admin
from django.contrib.auth.decorators import user_passes_test

@login_required
def orden_list(request):
    estado_filter = request.GET.get('estado', '')
    query = request.GET.get('q', '')
    
    ordenes = OrdenTrabajo.objects.all().order_by('-fecha_creacion')
    
    if estado_filter:
        ordenes = ordenes.filter(estado=estado_filter)
        
    if query:
        ordenes = ordenes.filter(numero_orden__icontains=query) | \
                  ordenes.filter(vehiculo__patente__icontains=query) | \
                  ordenes.filter(vehiculo__cliente__nombre_razon_social__icontains=query)
                  
    context = {
        'ordenes': ordenes,
        'query': query,
        'estado_filter': estado_filter,
        'estados': OrdenTrabajo.Estado.choices,
    }
    return render(request, 'ordenes/lista.html', context)

@login_required
def orden_detalle(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    context = {
        'orden': orden
    }
    return render(request, 'ordenes/detalle.html', context)

@login_required
@user_passes_test(es_admin)
def orden_create(request):
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.usuario_creador = request.user
            orden.save()
            messages.success(request, 'Orden creada con éxito.')
            return redirect('ordenes:detalle', pk=orden.pk)
    else:
        # Generar un numero de orden automatico (ej. OT-0001)
        ultimo = OrdenTrabajo.objects.order_by('-id').first()
        num = 1 if not ultimo else ultimo.id + 1
        form = OrdenTrabajoForm(initial={'numero_orden': f'OT-{num:04d}'})
    
    return render(request, 'ordenes/form.html', {'form': form, 'title': 'Nueva Orden'})

@login_required
def orden_update(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            messages.success(request, 'Orden actualizada.')
            return redirect('ordenes:detalle', pk=orden.pk)
    else:
        form = OrdenTrabajoForm(instance=orden)
    
    return render(request, 'ordenes/form.html', {'form': form, 'title': f'Editar Orden #{orden.numero_orden}'})

@login_required
def orden_iniciar(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    if orden.estado == 'PENDIENTE':
        orden.estado = 'EN_PROCESO'
        orden.save()
        messages.success(request, f'Orden {orden.numero_orden} iniciada.')
    return redirect('ordenes:detalle', pk=orden.pk)

from django.db import transaction
from apps.inventario.models import MovimientoStock

@login_required
def orden_completar(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    if orden.estado == 'EN_PROCESO':
        with transaction.atomic():
            orden.estado = 'COMPLETADA'
            orden.save()
            
            for detalle in orden.productos.all():
                producto = detalle.producto
                producto.stock_actual -= detalle.cantidad
                producto.save()
                
                MovimientoStock.objects.create(
                    producto=producto,
                    orden=orden,
                    tipo_movimiento='SALIDA',
                    cantidad=detalle.cantidad,
                    stock_resultante=producto.stock_actual,
                    motivo=f'Salida automática por Orden #{orden.numero_orden}',
                    usuario=request.user
                )
                
            messages.success(request, f'Orden {orden.numero_orden} marcada como completada y stock descontado.')
    return redirect('ordenes:detalle', pk=orden.pk)

from apps.facturas.models import Factura
from django.utils import timezone

@login_required
@user_passes_test(es_admin)
def orden_facturar(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    if orden.estado == 'COMPLETADA':
        with transaction.atomic():
            orden.estado = 'FACTURADA'
            orden.fecha_cierre = timezone.now()
            orden.save()
            
            # Generar factura
            ultimo_f = Factura.objects.order_by('-id').first()
            num_f = 1 if not ultimo_f else ultimo_f.id + 1
            
            Factura.objects.create(
                numero_factura=f'F-{num_f:05d}',
                orden=orden,
                cliente=orden.vehiculo.cliente,
                subtotal=orden.subtotal,
                iva=orden.iva,
                total=orden.total,
                saldo_pendiente=orden.total
            )
            
        messages.success(request, f'Orden {orden.numero_orden} facturada con éxito.')
    return redirect('ordenes:detalle', pk=orden.pk)

from .forms import DetalleServicioForm, DetalleProductoForm
from .models import DetalleServicio, DetalleProducto

@login_required
def servicio_add(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    if request.method == 'POST':
        form = DetalleServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.orden = orden
            servicio.save()
            orden.actualizar_totales()
            messages.success(request, 'Servicio agregado.')
            return redirect('ordenes:detalle', pk=orden.pk)
    else:
        form = DetalleServicioForm()
    return render(request, 'ordenes/detalle_form.html', {'form': form, 'title': 'Agregar Servicio', 'orden': orden})

@login_required
def producto_add(request, pk):
    orden = get_object_or_404(OrdenTrabajo, pk=pk)
    if request.method == 'POST':
        form = DetalleProductoForm(request.POST)
        if form.is_valid():
            producto_detalle = form.save(commit=False)
            producto_detalle.orden = orden
            producto_detalle.save()
            orden.actualizar_totales()
            messages.success(request, 'Producto agregado.')
            return redirect('ordenes:detalle', pk=orden.pk)
    else:
        form = DetalleProductoForm()
    return render(request, 'ordenes/detalle_form.html', {'form': form, 'title': 'Agregar Producto', 'orden': orden})

@login_required
def servicio_delete(request, pk):
    detalle = get_object_or_404(DetalleServicio, pk=pk)
    orden_pk = detalle.orden.pk
    orden = detalle.orden
    detalle.delete()
    orden.actualizar_totales()
    messages.success(request, 'Servicio eliminado.')
    return redirect('ordenes:detalle', pk=orden_pk)

@login_required
def producto_delete(request, pk):
    detalle = get_object_or_404(DetalleProducto, pk=pk)
    orden_pk = detalle.orden.pk
    orden = detalle.orden
    detalle.delete()
    orden.actualizar_totales()
    messages.success(request, 'Producto eliminado.')
    return redirect('ordenes:detalle', pk=orden_pk)
