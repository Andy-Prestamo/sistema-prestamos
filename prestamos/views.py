from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now
from .models import Cliente, Prestamo, Pago


def dashboard(request):

    total_clientes = Cliente.objects.count()

    total_prestado = Prestamo.objects.aggregate(
        total=Sum('monto')
    )['total'] or 0

    ganancia_total = Prestamo.objects.aggregate(
        total=Sum('ganancia')
    )['total'] or 0

    pendiente = Prestamo.objects.aggregate(
        total=Sum('saldo_pendiente')
    )['total'] or 0

    capital_recuperado = total_prestado + ganancia_total - pendiente

    pagos_hoy = Pago.objects.filter(
        fecha_pago=now().date()
    )

    total_pagos_hoy = pagos_hoy.aggregate(
        total=Sum('monto_pagado')
    )['total'] or 0

    context = {
        'total_clientes': total_clientes,
        'total_prestado': total_prestado,
        'ganancia_total': ganancia_total,
        'pendiente': pendiente,
        'capital_recuperado': capital_recuperado,
        'total_pagos_hoy': total_pagos_hoy,
        'pagos_hoy': pagos_hoy,
    }

    return render(request, 'dashboard.html', context)

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def pagos(request):
    pagos = Pago.objects.all()
    return render(request, 'pagos.html', {'pagos': pagos})