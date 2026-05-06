from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AlertaMantenimiento

@login_required
def alerta_list(request):
    estado_filter = request.GET.get('estado', 'PENDIENTE')
    query = request.GET.get('q', '')
    
    alertas = AlertaMantenimiento.objects.all().order_by('fecha_estimada')
    
    if estado_filter:
        alertas = alertas.filter(estado=estado_filter)
        
    if query:
        alertas = alertas.filter(vehiculo__patente__icontains=query) | \
                  alertas.filter(vehiculo__cliente__nombre_razon_social__icontains=query) | \
                  alertas.filter(tipo_servicio__nombre__icontains=query)
                  
    context = {
        'alertas': alertas,
        'query': query,
        'estado_filter': estado_filter,
        'estados': AlertaMantenimiento.Estado.choices,
    }
    return render(request, 'mantenimiento/alertas.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

@login_required
def alerta_notificar(request, pk):
    alerta = get_object_or_404(AlertaMantenimiento, pk=pk)
    if alerta.estado == 'PENDIENTE':
        alerta.estado = 'NOTIFICADA'
        alerta.fecha_notificacion = timezone.now()
        alerta.save()
        messages.success(request, f'Alerta para {alerta.vehiculo.patente} marcada como notificada.')
    return redirect('mantenimiento:alertas')
