from django.shortcuts import render
from .models import Cliente, Prestamo, Pago
from django.db.models import Sum
from django.utils.timezone import now

def dashboard(request):
    # Dinero que tu papá ha prestado (Capital puro)
    capital_en_calle = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('monto'))['monto__sum'] or 0
    
    # Lo que falta cobrar (Capital + Intereses pendientes)
    total_pendiente = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('saldo_pendiente'))['saldo_pendiente__sum'] or 0
    
    # Ganancia cobrada (Basado en pagos recibidos)
    # Para simplificar: Ganancia = Total Cobrado - Capital retornado (puedes ajustarlo luego)
    total_cobrado = Pago.objects.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0

    pagos_hoy = Pago.objects.filter(fecha_pago__date=now().date())

    context = {
        'pendiente': total_pendiente,
        'capital_invertido': capital_en_calle,
        'total_cobrado': total_cobrado,
        'pagos_hoy': pagos_hoy,
    }
    return render(request, 'dashboard.html', context)

def clientes(request):
    return render(request, 'clientes.html', {'clientes': Cliente.objects.all()})

def pagos(request):
    return render(request, 'pagos.html', {'pagos': Pago.objects.all().order_by('-fecha_pago')})

def prestamos_lista(request):
    return render(request, 'prestamos.html', {'prestamos': Prestamo.objects.all()})