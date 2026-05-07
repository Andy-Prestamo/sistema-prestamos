from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now

from .models import Cliente, Prestamo, Pago


# =========================
# DASHBOARD PRINCIPAL
# =========================
def dashboard(request):

    # TOTAL CLIENTES
    total_clientes = Cliente.objects.count()

    # TOTAL PRESTADO
    total_prestado = Prestamo.objects.aggregate(
        total=Sum('monto')
    )['total'] or 0

    # GANANCIA TOTAL
    ganancia_total = Prestamo.objects.aggregate(
        total=Sum('ganancia')
    )['total'] or 0

    # TOTAL PENDIENTE
    pendiente = Prestamo.objects.aggregate(
        total=Sum('saldo_pendiente')
    )['total'] or 0

    # CAPITAL RECUPERADO
    capital_recuperado = (
        total_prestado +
        ganancia_total -
        pendiente
    )

    # PAGOS DEL DIA
    pagos_hoy = Pago.objects.filter(
        fecha_pago=now().date()
    )

    # TOTAL PAGOS HOY
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

    return render(
        request,
        'dashboard.html',
        context
    )