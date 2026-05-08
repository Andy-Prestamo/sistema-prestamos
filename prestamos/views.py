from django.shortcuts import render
from .models import Cliente, Prestamo, Pago
from django.db.models import Sum
import datetime

def dashboard(request):
    # 1. CAPITAL EN LA CALLE: Suma de lo que papá prestó originalmente (solo préstamos activos)
    capital_en_calle = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('monto'))['monto__sum'] or 0
    
    # 2. DINERO POR COBRAR: Lo que falta recuperar (Capital + Interés que aún no pagan)
    total_pendiente = Prestamo.objects.filter(estado_pagado=False).aggregate(Sum('saldo_pendiente'))['saldo_pendiente__sum'] or 0
    
    # 3. CAPITAL RECUPERADO: Todo el dinero que ya entró a la mano de papá
    total_cobrado = Pago.objects.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0

    # 4. PAGOS DE HOY: Filtro seguro para evitar errores de zona horaria en SQLite
    hoy = datetime.date.today()
    pagos_hoy = Pago.objects.filter(
        fecha_pago__year=hoy.year, 
        fecha_pago__month=hoy.month, 
        fecha_pago__day=hoy.day
    ).order_by('-fecha_pago')

    context = {
        'pendiente': total_pendiente,
        'capital_invertido': capital_en_calle,
        'total_cobrado': total_cobrado,
        'pagos_hoy': pagos_hoy,
    }
    return render(request, 'dashboard.html', context)

def clientes(request):
    # Lista de todos los clientes registrados
    return render(request, 'clientes.html', {'clientes': Cliente.objects.all()})

def pagos(request):
    # Historial completo de cobros realizados
    return render(request, 'pagos.html', {'pagos': Pago.objects.all().order_by('-fecha_pago')})

def prestamos_lista(request):
    # Lista de préstamos para ver quién debe y quién no
    return render(request, 'prestamos.html', {'prestamos': Prestamo.objects.all()})