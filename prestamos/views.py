from django.shortcuts import render, redirect, get_object_ some_or_404
from .models import Cliente, Prestamo, Pago
from .forms import ClienteForm, PrestamoForm, PagoForm
from django.db.models import Sum
from django.utils import timezone
import datetime

# --- DASHBOARD ---
def dashboard(request):
    capital_en_calle = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('monto'))['monto__sum'] or 0
    total_pendiente = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('saldo_pendiente'))['saldo_pendiente__sum'] or 0
    total_cobrado = Pago.objects.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0
    
    hoy = timezone.now().date()
    inicio_dia = timezone.make_aware(datetime.datetime.combine(hoy, datetime.time.min))
    fin_dia = timezone.make_aware(datetime.datetime.combine(hoy, datetime.time.max))
    pagos_hoy = Pago.objects.filter(fecha_pago__range=(inicio_dia, fin_dia)).order_by('-fecha_pago')

    return render(request, 'dashboard.html', {
        'pendiente': total_pendiente, 'capital_invertido': capital_en_calle,
        'total_cobrado': total_cobrado, 'pagos_hoy': pagos_hoy,
    })

# --- GESTIÓN DE CLIENTES ---
def clientes(request):
    return render(request, 'clientes.html', {'clientes': Cliente.objects.all()})

def crear_cliente(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('clientes')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Nuevo Cliente'})

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

# --- GESTIÓN DE PRÉSTAMOS ---
def prestamos_lista(request):
    return render(request, 'prestamos.html', {'prestamos': Prestamo.objects.all().order_by('-fecha_inicio')})

def crear_prestamo(request):
    form = PrestamoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('prestamos_lista')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Nuevo Préstamo'})

def eliminar_prestamo(request, pk):
    obj = get_object_or_404(Prestamo, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('prestamos_lista')
    return render(request, 'confirmar_eliminar.html', {'obj': obj})

# --- GESTIÓN DE PAGOS ---
def registrar_pago(request):
    form = PagoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Registrar Cobro'})