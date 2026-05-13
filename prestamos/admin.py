from django.contrib import admin
from .models import Cliente, Prestamo, Pago

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'lugar', 'telefono')
    search_fields = ('nombre', 'lugar')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    # Usamos solo los nombres de campos que existen en tu nuevo models.py
    list_display = ('cliente', 'monto', 'total_a_pagar', 'saldo_pendiente', 'tipo_cuota', 'fecha_inicio', 'estado_pagado')
    list_filter = ('tipo_cuota', 'estado_pagado')
    search_fields = ('cliente__nombre',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('prestamo', 'monto_pagado', 'fecha_pago')
    list_filter = ('fecha_pago',)