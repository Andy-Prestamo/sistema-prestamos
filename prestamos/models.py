from django.db import models
from django.utils import timezone
from decimal import Decimal

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    OPCIONES_CUOTA = [
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('quincenal', 'Quincenal'),
        ('mensual', 'Mensual'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    interes_porcentaje = models.FloatField(default=20.0)
    total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    tipo_cuota = models.CharField(max_length=20, choices=OPCIONES_CUOTA, default='diario')
    fecha_inicio = models.DateField(auto_now_add=True)
    estado_pagado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        porcentaje = Decimal(str(self.interes_porcentaje)) / Decimal('100')
        self.total_a_pagar = self.monto * (Decimal('1') + porcentaje)
        if not self.pk:
            self.saldo_pendiente = self.total_a_pagar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente.nombre} | Debe: S/ {self.saldo_pendiente}"

class Pago(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='pagos')
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        p = self.prestamo
        p.saldo_pendiente -= self.monto_pagado
        if p.saldo_pendiente <= 0:
            p.saldo_pendiente = 0
            p.estado_pagado = True
        p.save()