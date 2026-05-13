from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # IMPORTANTE
from django.db.models import Sum, F
from .models import Cliente, Prestamo, Pago
from .forms import ClienteForm, PrestamoForm, PagoForm
from django.utils import timezone


@login_required
def dashboard(request):
    # --- MÉTRICAS DE DINERO EN LA CALLE (ACTUAL) ---
    prestamos_activos = Prestamo.objects.filter(estado_pagado=False)
    capital_en_calle = prestamos_activos.aggregate(Sum('monto'))['monto__sum'] or 0
    ganancia_proyectada = prestamos_activos.aggregate(
        total=Sum(F('total_a_pagar') - F('monto'))
    )['total'] or 0

    # --- MÉTRICAS DE CRECIMIENTO REAL (HISTÓRICO) ---
    # 1. Total de todos los intereses cobrados de préstamos ya terminados
    prestamos_pagados = Prestamo.objects.filter(estado_pagado=True)
    ganancias_reales = prestamos_pagados.aggregate(
        total=Sum(F('total_a_pagar') - F('monto'))
    )['total'] or 0

    # 2. Total de dinero que ha pasado por el sistema (Capital + Ganancias)
    todos_los_pagos = Pago.objects.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0

    # --- MÉTRICAS DEL DÍA ---
    hoy_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    hoy_fin = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    pagos_hoy = Pago.objects.filter(fecha_pago__range=(hoy_inicio, hoy_fin)).order_by('-fecha_pago')
    total_hoy = pagos_hoy.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0

    return render(request, 'dashboard.html', {
        'capital_en_calle': capital_en_calle,
        'ganancia_proyectada': ganancia_proyectada,
        'ganancias_reales': ganancias_reales, # <--- Nueva métrica
        'total_recaudado_historico': todos_los_pagos, # <--- Nueva métrica
        'pagos_hoy': pagos_hoy,
        'total_hoy': total_hoy,
    })

@login_required
def historial_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    prestamos = Prestamo.objects.filter(cliente=cliente).order_by('-fecha_inicio')
    pagos = Pago.objects.filter(prestamo__cliente=cliente).order_by('-fecha_pago')
    return render(request, 'detalle_cliente.html', {'cliente': cliente, 'prestamos': prestamos, 'pagos': pagos})

@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    form = ClienteForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Nuevo Cliente'})

@login_required
def crear_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    form = PrestamoForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Nuevo Préstamo'})

@login_required
def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PagoForm()
        # ESTO ES LO IMPORTANTE: 
        # Filtramos para que solo aparezcan préstamos que NO estén pagados
        form.fields['prestamo'].queryset = Prestamo.objects.filter(estado_pagado=False)
        
    return render(request, 'formulario.html', {
        'form': form, 
        'titulo': 'Registrar Pago'
    })

@login_required
def editar_cliente(request, pk):
    obj = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('clientes')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Editar Cliente'})

@login_required
def eliminar_cliente(request, pk):
    obj = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('clientes')
    return render(request, 'confirmar_eliminar.html', {'obj': obj})

@login_required
def eliminar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    prestamo = pago.prestamo
    cliente_pk = prestamo.cliente.pk
    
    # Revertimos el saldo sumando el monto del pago eliminado
    prestamo.saldo_pendiente += pago.monto_pagado
    
    # Si el préstamo estaba marcado como pagado (True), lo volvemos a poner pendiente (False)
    if prestamo.saldo_pendiente > 0:
        prestamo.estado_pagado = False
        
    prestamo.save()
    pago.delete()
    
    # Redirige de vuelta al historial del cliente
    return redirect('historial_cliente', pk=cliente_pk)