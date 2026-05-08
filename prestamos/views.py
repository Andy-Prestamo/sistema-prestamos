from django.shortcuts import render
from .models import Cliente, Prestamo, Pago
from django.db.models import Sum
from django.utils import timezone
import datetime

def dashboard(request):
    # 1. Cálculos de dinero
    capital_en_calle = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('monto'))['monto__sum'] or 0
    total_pendiente = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('saldo_pendiente'))['saldo_pendiente__sum'] or 0
    total_cobrado = Pago.objects.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0

    # 2. FILTRO DE HOY (MÉTODO SEGURO POR RANGO)
    # Esto crea un rango desde las 00:00:00 hasta las 23:59:59 de hoy
    hoy = timezone.now().date()
    inicio_dia = timezone.make_aware(datetime.datetime.combine(hoy, datetime.time.min))
    fin_dia = timezone.make_aware(datetime.datetime.combine(hoy, datetime.time.max))
    
    # Filtramos usando 'range', que es compatible con TODAS las bases de datos
    pagos_hoy = Pago.objects.filter(fecha_pago__range=(inicio_dia, fin_dia)).order_by('-fecha_pago')

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