from django.db import models
from django.contrib.auth.models import User


MESES = [
    (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
    (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
    (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre'),
]

TIPO_CHOICES = [
    ('ingreso', 'Ingreso'),
    ('gasto', 'Gasto'),
]


class Balance(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='balances'
    )
    mes = models.PositiveSmallIntegerField(choices=MESES)
    anio = models.PositiveIntegerField(verbose_name='Año')
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'mes', 'anio')
        ordering = ['-anio', '-mes']
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'

    def __str__(self):
        return f"{self.get_mes_display()} {self.anio} – {self.usuario.username}"

    @property
    def total_ingresos(self):
        return sum(t.monto for t in self.transacciones.filter(tipo='ingreso'))

    @property
    def total_gastos(self):
        return sum(t.monto for t in self.transacciones.filter(tipo='gasto'))

    @property
    def saldo_final(self):
        return self.saldo_inicial + self.total_ingresos - self.total_gastos


class Transaccion(models.Model):
    balance = models.ForeignKey(
        Balance, on_delete=models.CASCADE, related_name='transacciones'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f"{self.tipo} | {self.categoria} | ${self.monto}"
