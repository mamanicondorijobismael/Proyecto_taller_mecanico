from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehiculo
from .forms import VehiculoForm

@login_required
def vehiculo_list(request):
    query = request.GET.get('q', '')
    if query:
        vehiculos = Vehiculo.objects.filter(patente__icontains=query) | \
                    Vehiculo.objects.filter(marca__icontains=query) | \
                    Vehiculo.objects.filter(modelo__icontains=query) | \
                    Vehiculo.objects.filter(cliente__nombre_razon_social__icontains=query)
    else:
        vehiculos = Vehiculo.objects.all()
    
    context = {
        'vehiculos': vehiculos,
        'query': query
    }
    return render(request, 'vehiculos/lista.html', context)

@login_required
def vehiculo_create(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo registrado con éxito.')
            return redirect('vehiculos:lista')
        else:
            messages.error(request, 'Error al registrar el vehículo. Revisa los datos.')
    else:
        form = VehiculoForm()
    
    context = {'form': form, 'title': 'Nuevo Vehículo'}
    return render(request, 'vehiculos/form.html', context)

@login_required
def vehiculo_update(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado con éxito.')
            return redirect('vehiculos:lista')
        else:
            messages.error(request, 'Error al actualizar el vehículo. Revisa los datos.')
    else:
        form = VehiculoForm(instance=vehiculo)
    
    context = {'form': form, 'title': 'Editar Vehículo'}
    return render(request, 'vehiculos/form.html', context)
