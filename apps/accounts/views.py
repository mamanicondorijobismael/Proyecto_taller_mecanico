from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from django.db import models
from datetime import timedelta
from apps.ordenes.models import OrdenTrabajo
from apps.inventario.models import ProductoBase
from apps.mantenimiento.models import AlertaMantenimiento

@login_required
def dashboard(request):
    hoy = timezone.now()
    inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # KPI data
    ordenes_mes = OrdenTrabajo.objects.filter(fecha_creacion__gte=inicio_mes, estado__in=['COMPLETADA', 'FACTURADA'])
    ingresos_mes = ordenes_mes.aggregate(total_ingresos=Sum('total'))['total_ingresos'] or 0
    
    costos_mes = 0 # Can be calculated by summing cost of products in those orders
    
    ordenes_activas = OrdenTrabajo.objects.filter(estado__in=['PENDIENTE', 'EN_PROCESO', 'PAUSADA']).count()
    
    productos_criticos_qs = ProductoBase.objects.filter(stock_actual__lte=models.F('stock_minimo'), activo=True)
    stock_critico = productos_criticos_qs.count()
    
    alertas_mantenimiento_qs = AlertaMantenimiento.objects.filter(estado='PENDIENTE')
    alertas_count = alertas_mantenimiento_qs.count()
    
    ganancia_neta = ingresos_mes - costos_mes
    ordenes_completadas = ordenes_mes.count()
    ticket_promedio = ingresos_mes / ordenes_completadas if ordenes_completadas > 0 else 0

    kpi = {
        'ingresos_mes': ingresos_mes,
        'costos_mes': costos_mes,
        'ganancia_neta': ganancia_neta,
        'ticket_promedio': ticket_promedio,
        'ordenes_completadas': ordenes_completadas,
        'ordenes_activas': ordenes_activas,
        'stock_critico': stock_critico,
        'alertas_mantenimiento': alertas_count,
    }

    ordenes_recientes = OrdenTrabajo.objects.all().order_by('-fecha_creacion')[:5]
    productos_criticos = productos_criticos_qs[:5]
    alertas_mantenimiento = alertas_mantenimiento_qs[:5]

    context = {
        'kpi': kpi,
        'ordenes_recientes': ordenes_recientes,
        'productos_criticos': productos_criticos,
        'alertas_mantenimiento': alertas_mantenimiento,
    }
    return render(request, 'dashboard.html', context)


from .models import Usuario
from .forms import UsuarioCustomCreationForm, UsuarioCustomChangeForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .decorators import es_dueno
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(es_dueno)
def usuario_list(request):
    usuarios = Usuario.objects.all().order_by('-fecha_creacion')
    return render(request, 'accounts/usuarios_lista.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_dueno)
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioCustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('usuarios_lista')
    else:
        form = UsuarioCustomCreationForm()
    return render(request, 'accounts/usuario_form.html', {'form': form, 'title': 'Nuevo Usuario'})

@login_required
@user_passes_test(es_dueno)
def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioCustomChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado con éxito.')
            return redirect('usuarios_lista')
    else:
        form = UsuarioCustomChangeForm(instance=usuario)
    return render(request, 'accounts/usuario_form.html', {'form': form, 'title': 'Editar Usuario'})
