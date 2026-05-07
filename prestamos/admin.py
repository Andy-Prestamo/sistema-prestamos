from django.contrib import admin
from django.db.models import Sum
from decimal import Decimal

from .models import Cliente, Prestamo, Pago


# =========================
# PAGOS DENTRO DEL PRESTAMO
# =========================
class PagoInline(admin.TabularInline):

    model = Pago

    extra = 1


# =========================
# ADMIN PRESTAMOS
# =========================
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):

    list_display = (
        'cliente',
        'monto',
        'ganancia',
        'total',
        'saldo_pendiente',
        'tipo_pago',
        'estado',
        'fecha'
    )

    search_fields = (
        'cliente__nombre',
    )

    list_filter = (
        'estado',
        'tipo_pago'
    )

    inlines = [PagoInline]


# =========================
# ADMIN CLIENTES
# =========================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'telefono',
        'dni'
    )

    search_fields = (
        'nombre',
    )


# =========================
# HISTORIAL PAGOS
# =========================
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):

    list_display = (
        'cliente',
        'monto_pagado',
        'fecha_pago',
        'saldo_restante',
        'ganancia_generada'
    )

    search_fields = (
        'prestamo__cliente__nombre',
    )

    list_filter = (
        'fecha_pago',
    )

    def cliente(self, obj):
        return obj.prestamo.cliente.nombre

    def saldo_restante(self, obj):
        return obj.prestamo.saldo_pendiente

    def ganancia_generada(self, obj):

        return (
            obj.monto_pagado -
            obj.prestamo.cuota
        )


# =========================
# TITULOS PANEL
# =========================
admin.site.site_header = "Sistema de Préstamos"

admin.site.site_title = "Administración"

admin.site.index_title = "Panel Administrativo"