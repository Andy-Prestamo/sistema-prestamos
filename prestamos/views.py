from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import Cliente, Prestamo, Pago
from .forms import ClienteForm, PrestamoForm, PagoForm
from django.utils import timezone
from datetime import datetime, time

def dashboard(request):
    # Capital e intereses
    capital = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('monto'))['monto__sum'] or 0
    pendiente = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('saldo_pendiente'))['saldo_pendiente__sum'] or 0
    ganancia_proyectada = Prestamo.objects.filter(estado_pagado=False).aggregate(
        total=Sum(F('total_a_pagar') - F('monto'))
    )['total'] or 0
    
    # Fix para SQLite: Filtrar por rango de tiempo en lugar de __date
    hoy_inicio = timezone.make_aware(datetime.combine(timezone.now().date(), time.min))
    pagos_hoy = Pago.objects.filter(fecha_pago__gte=hoy_inicio).order_by('-fecha_pago')
    total_hoy = pagos_hoy.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0

    return render(request, 'dashboard.html', {
        'capital_invertido': capital,
        'pendiente': pendiente,
        'ganancia_proyectada': ganancia_proyectada,
        'pagos_hoy': pagos_hoy,
        'total_hoy': total_hoy
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

def historial_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    prestamos = Prestamo.objects.filter(cliente=cliente).order_by('-fecha_inicio')
    pagos = Pago.objects.filter(prestamo__cliente=cliente).order_by('-fecha_pago')
    return render(request, 'detalle_cliente.html', {'cliente': cliente, 'prestamos': prestamos, 'pagos': pagos})

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