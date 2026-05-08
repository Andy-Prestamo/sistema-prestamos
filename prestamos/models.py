from django.db import models
from decimal import Decimal
from django.db.models import Sum

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    dni = models.CharField(max_length=8, blank=True, null=True, verbose_name="DNI")
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    TIPO_PAGO = [('diario', 'Diario'), ('semanal', 'Semanal'), ('quincenal', 'Quincenal'), ('mensual', 'Mensual')]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Prestado (S/) ")
    interes_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, verbose_name="Interés %")
    total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    tipo_cuota = models.CharField(max_length=15, choices=TIPO_PAGO, default='diario')
    fecha_inicio = models.DateField(auto_now_add=True)
    estado_pagado = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        # Cálculo automático: Monto + 20%
        if not self.pk:
            self.total_a_pagar = self.monto * (1 + (self.interes_porcentaje / 100))
            self.saldo_pendiente = self.total_a_pagar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente.nombre} | Debe: S/ {self.saldo_pendiente}"

class Pago(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='pagos')
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto que recibe Papá (S/) ")
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar el saldo del préstamo automáticamente
        p = self.prestamo
        total_cobrado = p.pagos.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0
        p.saldo_pendiente = p.total_a_pagar - total_cobrado
        if p.saldo_pendiente <= 0:
            p.estado_pagado = True
            p.saldo_pendiente = 0
        p.save()