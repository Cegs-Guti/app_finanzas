from django.contrib import admin
from .models import Balance, Transaccion


class TransaccionInline(admin.TabularInline):
    model = Transaccion
    extra = 0


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mes', 'anio', 'saldo_inicial', 'creado')
    list_filter = ('mes', 'anio', 'usuario')
    inlines = [TransaccionInline]


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('balance', 'tipo', 'categoria', 'monto', 'creado')
    list_filter = ('tipo', 'categoria')
