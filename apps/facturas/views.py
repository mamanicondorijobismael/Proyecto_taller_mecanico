from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Factura
from apps.accounts.decorators import es_admin
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(es_admin)
def factura_list(request):
    # ... (existing code remains same)
    # I'll keep the logic I saw before
    estado_filter = request.GET.get('estado', '')
    query = request.GET.get('q', '')
    
    facturas = Factura.objects.all().order_by('-fecha_emision')
    
    if estado_filter:
        facturas = facturas.filter(estado_pago=estado_filter)
        
    if query:
        facturas = facturas.filter(numero_factura__icontains=query) | \
                   facturas.filter(cliente__nombre_razon_social__icontains=query)
                   
    context = {
        'facturas': facturas,
        'query': query,
        'estado_filter': estado_filter,
        'estados': Factura.EstadoPago.choices,
    }
    return render(request, 'facturas/lista.html', context)

from django.shortcuts import redirect
from django.contrib import messages

@login_required
@user_passes_test(es_admin)
def factura_pagar(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if factura.estado_pago != 'PAGADA':
        factura.estado_pago = 'PAGADA'
        factura.saldo_pendiente = 0
        factura.save()
        messages.success(request, f'Factura {factura.numero_factura} marcada como pagada.')
    return redirect('facturas:lista')
