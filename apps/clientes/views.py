from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm

@login_required
def cliente_list(request):
    query = request.GET.get('q', '')
    if query:
        clientes = Cliente.objects.filter(nombre_razon_social__icontains=query) | Cliente.objects.filter(documento__icontains=query)
    else:
        clientes = Cliente.objects.all()
    
    context = {
        'clientes': clientes,
        'query': query
    }
    return render(request, 'clientes/lista.html', context)

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado con éxito.')
            return redirect('clientes:lista')
        else:
            messages.error(request, 'Error al crear el cliente. Revisa los datos.')
    else:
        form = ClienteForm()
    
    context = {'form': form, 'title': 'Nuevo Cliente'}
    return render(request, 'clientes/form.html', context)

@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado con éxito.')
            return redirect('clientes:lista')
        else:
            messages.error(request, 'Error al actualizar el cliente. Revisa los datos.')
    else:
        form = ClienteForm(instance=cliente)
    
    context = {'form': form, 'title': 'Editar Cliente'}
    return render(request, 'clientes/form.html', context)
