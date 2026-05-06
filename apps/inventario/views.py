from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProductoBase, RepuestoGenerico, Neumatico

@login_required
def producto_list(request):
    query = request.GET.get('q', '')
    critico = request.GET.get('critico', '')
    
    productos = ProductoBase.objects.all().order_by('-fecha_creacion')
    if query:
        productos = productos.filter(nombre__icontains=query) | productos.filter(codigo_sku__icontains=query)
    
    if critico == '1':
        from django.db.models import F
        productos = productos.filter(stock_actual__lte=F('stock_minimo'))
        
    context = {
        'productos': productos,
        'query': query,
        'critico': critico
    }
    return render(request, 'inventario/lista.html', context)

@login_required
def repuesto_list(request):
    query = request.GET.get('q', '')
    if query:
        repuestos = RepuestoGenerico.objects.filter(nombre__icontains=query) | \
                    RepuestoGenerico.objects.filter(codigo_sku__icontains=query) | \
                    RepuestoGenerico.objects.filter(marca_repuesto__icontains=query)
        repuestos = repuestos.order_by('-fecha_creacion')
    else:
        repuestos = RepuestoGenerico.objects.all().order_by('-fecha_creacion')
        
    context = {
        'repuestos': repuestos,
        'query': query
    }
    return render(request, 'inventario/repuestos.html', context)

@login_required
def neumatico_list(request):
    query = request.GET.get('q', '')
    if query:
        neumaticos = Neumatico.objects.filter(nombre__icontains=query) | \
                     Neumatico.objects.filter(codigo_sku__icontains=query) | \
                     Neumatico.objects.filter(marca_neumatico__icontains=query)
        neumaticos = neumaticos.order_by('-fecha_creacion')
    else:
        neumaticos = Neumatico.objects.all().order_by('-fecha_creacion')
        
    context = {
        'neumaticos': neumaticos,
        'query': query
    }
    return render(request, 'inventario/neumaticos.html', context)

from .forms import RepuestoForm, NeumaticoForm
from apps.accounts.decorators import es_admin
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(es_admin)
def repuesto_create(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Repuesto agregado con éxito.')
            return redirect('inventario:repuestos')
    else:
        form = RepuestoForm()
    return render(request, 'inventario/form.html', {'form': form, 'title': 'Nuevo Repuesto', 'return_url': 'inventario:repuestos'})

@login_required
@user_passes_test(es_admin)
def repuesto_update(request, pk):
    repuesto = get_object_or_404(RepuestoGenerico, pk=pk)
    if request.method == 'POST':
        form = RepuestoForm(request.POST, instance=repuesto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Repuesto actualizado.')
            return redirect('inventario:repuestos')
    else:
        form = RepuestoForm(instance=repuesto)
    return render(request, 'inventario/form.html', {'form': form, 'title': 'Editar Repuesto', 'return_url': 'inventario:repuestos'})

@login_required
@user_passes_test(es_admin)
def neumatico_create(request):
    if request.method == 'POST':
        form = NeumaticoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Neumático agregado con éxito.')
            return redirect('inventario:neumaticos')
    else:
        form = NeumaticoForm()
    return render(request, 'inventario/form.html', {'form': form, 'title': 'Nuevo Neumático', 'return_url': 'inventario:neumaticos'})

@login_required
@user_passes_test(es_admin)
def neumatico_update(request, pk):
    neumatico = get_object_or_404(Neumatico, pk=pk)
    if request.method == 'POST':
        form = NeumaticoForm(request.POST, instance=neumatico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Neumático actualizado.')
            return redirect('inventario:neumaticos')
    else:
        form = NeumaticoForm(instance=neumatico)
    return render(request, 'inventario/form.html', {'form': form, 'title': 'Editar Neumático', 'return_url': 'inventario:neumaticos'})
