from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Reserva
from django.utils import timezone

@login_required
def reserva_list(request):
    hoy = timezone.now().date()
    query = request.GET.get('q', '')
    
    reservas = Reserva.objects.all().order_by('-fecha_hora')
    
    if query:
        reservas = reservas.filter(cliente__nombre_razon_social__icontains=query) | \
                   reservas.filter(vehiculo__patente__icontains=query) | \
                   reservas.filter(servicio_solicitado__icontains=query)
                   
    context = {
        'reservas': reservas,
        'query': query,
        'hoy': hoy
    }
    return render(request, 'reservas/lista.html', context)
