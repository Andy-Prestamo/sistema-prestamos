from django.db import models
from decimal import Decimal
from django.db.models import Sum


# =========================
# CLIENTES
# =========================
class Cliente(models.Model):

    nombre = models.CharField(max_length=100)

    dni = models.CharField(
        max_length=8,
        blank=True,
        null=True
    )

    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nombre


# =========================
# PRESTAMOS
# =========================
class Prestamo(models.Model):

    TIPO_PAGO = [
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('quincenal', 'Quincenal'),
        ('mensual', 'Mensual'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    interes = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.20')
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    ganancia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    saldo_pendiente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    tipo_pago = models.CharField(
        max_length=15,
        choices=TIPO_PAGO
    )

    plazo = models.IntegerField()

    cuota = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    fecha = models.DateField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )

    def save(self, *args, **kwargs):

        # CALCULAR TOTAL
        self.total = self.monto * (
            Decimal('1.00') + self.interes
        )

        # GANANCIA
        self.ganancia = self.total - self.monto

        super().save(*args, **kwargs)

        # SUMAR PAGOS
        total_pagado = self.pago_set.aggregate(
            total=Sum('monto_pagado')
        )['total'] or Decimal('0')

        # SALDO PENDIENTE
        self.saldo_pendiente = self.total - total_pagado

        # ESTADO AUTOMATICO
        if self.saldo_pendiente <= 0:
            self.estado = 'pagado'
            self.saldo_pendiente = 0
        else:
            self.estado = 'pendiente'

        super().save(update_fields=[
            'saldo_pendiente',
            'estado'
        ])

    def __str__(self):
        return f"{self.cliente.nombre}"


# =========================
# PAGOS
# =========================
class Pago(models.Model):

    prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE
    )

    monto_pagado = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    fecha_pago = models.DateField()

    def save(self, *args, **kwargs):

        # GUARDAR PAGO
        super().save(*args, **kwargs)

        # SUMAR TODOS LOS PAGOS
        total_pagado = Pago.objects.filter(
            prestamo=self.prestamo
        ).aggregate(
            total=Sum('monto_pagado')
        )['total'] or 0

        # RECALCULAR SALDO
        self.prestamo.saldo_pendiente = (
            self.prestamo.total - total_pagado
        )

        # ACTUALIZAR ESTADO
        if self.prestamo.saldo_pendiente <= 0:

            self.prestamo.estado = 'pagado'

            self.prestamo.saldo_pendiente = 0

        else:

            self.prestamo.estado = 'pendiente'

        # GUARDAR PRESTAMO
        self.prestamo.save()

    def __str__(self):

        return f"{self.prestamo.cliente.nombre} - {self.monto_pagado}"