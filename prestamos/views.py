from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import Cliente, Prestamo, Pago
from .forms import ClienteForm, PrestamoForm, PagoForm
from django.utils import timezone
from datetime import datetime, time

def dashboard(request):
    # Préstamos activos
    prestamos_activos = Prestamo.objects.filter(estado_pagado=False)
    
    capital = prestamos_activos.aggregate(Sum('monto'))['monto__sum'] or 0
    ganancia_proyectada = prestamos_activos.aggregate(
        total=Sum(F('total_a_pagar') - F('monto'))
    )['total'] or 0
    
    # --- FILTRO COMPATIBLE CON SQLITE ---
    # En lugar de __date, usamos un rango: desde las 00:00:00 hasta ahora
    hoy_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    hoy_fin = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    
    pagos_hoy = Pago.objects.filter(fecha_pago__range=(hoy_inicio, hoy_fin)).order_by('-fecha_pago')
    
    # Sumar los cobros del día
    total_cobrado_hoy = pagos_hoy.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0

    return render(request, 'dashboard.html', {
        'capital_invertido': capital,
        'ganancia_proyectada': ganancia_proyectada,
        'pagos_hoy': pagos_hoy,
        'total_hoy': total_cobrado_hoy,
    })

def historial_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    prestamos = Prestamo.objects.filter(cliente=cliente).order_by('-fecha_inicio')
    pagos = Pago.objects.filter(prestamo__cliente=cliente).order_by('-fecha_pago')
    return render(request, 'detalle_cliente.html', {
        'cliente': cliente, 
        'prestamos': prestamos, 
        'pagos': pagos
    })

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Nuevo Cliente'})

def crear_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PrestamoForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Nuevo Préstamo'})

def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PagoForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Registrar Pago'})

def editar_cliente(request, pk):
    obj = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('clientes')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Editar Cliente'})

def eliminar_cliente(request, pk):
    obj = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('clientes')
    return render(request, 'confirmar_eliminar.html', {'obj': obj})