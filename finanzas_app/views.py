import json
import datetime
from decimal import Decimal
from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Balance, Transaccion, MESES
from .forms import (
    BalanceForm, TransaccionForm,
    SimuladorTransaccionForm, SimuladorInicioForm,
)

SESSION_KEY = 'simulador_balance'


def _get_sim(request):
    return request.session.get(SESSION_KEY, {
        'saldo_inicial': '0',
        'transacciones': [],
    })


def simulador(request):
    sim = _get_sim(request)

    if request.method == 'POST' and 'set_saldo' in request.POST:
        form_inicio = SimuladorInicioForm(request.POST)
        if form_inicio.is_valid():
            sim['saldo_inicial'] = str(form_inicio.cleaned_data['saldo_inicial'])
            sim['transacciones'] = []
            request.session[SESSION_KEY] = sim
            messages.success(request, 'Saldo inicial actualizado.')
            return redirect('finanzas:simulador')
    else:
        form_inicio = SimuladorInicioForm(
            initial={'saldo_inicial': sim['saldo_inicial']}
        )

    if request.method == 'POST' and 'add_transaccion' in request.POST:
        form_tx = SimuladorTransaccionForm(request.POST)
        if form_tx.is_valid():
            tx = {
                'tipo': form_tx.cleaned_data['tipo'],
                'categoria': form_tx.cleaned_data['categoria'],
                'descripcion': form_tx.cleaned_data['descripcion'],
                'monto': str(form_tx.cleaned_data['monto']),
            }
            sim['transacciones'].append(tx)
            request.session[SESSION_KEY] = sim
            messages.success(request, 'Transacción agregada.')
            return redirect('finanzas:simulador')
    else:
        form_tx = SimuladorTransaccionForm()

    saldo_inicial = Decimal(sim['saldo_inicial'])
    transacciones = sim['transacciones']
    total_ingresos = sum(Decimal(t['monto']) for t in transacciones if t['tipo'] == 'ingreso')
    total_gastos = sum(Decimal(t['monto']) for t in transacciones if t['tipo'] == 'gasto')
    saldo_final = saldo_inicial + total_ingresos - total_gastos

    return render(request, 'finanzas_app/simulador.html', {
        'form_inicio': form_inicio,
        'form_tx': form_tx,
        'transacciones': transacciones,
        'saldo_inicial': saldo_inicial,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'saldo_final': saldo_final,
    })


def simulador_eliminar_tx(request, idx):
    sim = _get_sim(request)
    try:
        sim['transacciones'].pop(int(idx))
        request.session[SESSION_KEY] = sim
        messages.success(request, 'Transacción eliminada.')
    except (IndexError, ValueError):
        messages.error(request, 'Transacción no encontrada.')
    return redirect('finanzas:simulador')


def simulador_limpiar(request):
    if SESSION_KEY in request.session:
        del request.session[SESSION_KEY]
    messages.info(request, 'Simulación reiniciada.')
    return redirect('finanzas:simulador')


@login_required
def simulador_guardar(request):
    sim = _get_sim(request)
    if not sim['transacciones']:
        messages.warning(request, 'No hay transacciones para guardar.')
        return redirect('finanzas:simulador')

    if request.method == 'POST':
        form = BalanceForm(request.POST, usuario=request.user)
        if form.is_valid():
            balance = form.save(commit=False)
            balance.usuario = request.user
            balance.saldo_inicial = Decimal(sim['saldo_inicial'])
            balance.save()
            for tx in sim['transacciones']:
                Transaccion.objects.create(
                    balance=balance,
                    tipo=tx['tipo'],
                    categoria=tx['categoria'],
                    descripcion=tx.get('descripcion', ''),
                    monto=Decimal(tx['monto']),
                )
            if SESSION_KEY in request.session:
                del request.session[SESSION_KEY]
            messages.success(request, f'Balance guardado: {balance}')
            return redirect('finanzas:detalle', pk=balance.pk)
    else:
        hoy = datetime.date.today()
        form = BalanceForm(
            initial={'mes': hoy.month, 'anio': hoy.year},
            usuario=request.user,
        )

    return render(request, 'finanzas_app/simulador_guardar.html', {'form': form})


@login_required
def dashboard(request):
    """
    Dashboard principal con historial filtrable por año y gráfico
    de barras de gastos por categoría del mes seleccionado.
    """
    todos_balances = Balance.objects.filter(usuario=request.user)

    
    anios_disponibles = sorted(
        todos_balances.values_list('anio', flat=True).distinct(),
        reverse=True
    )

    
    anio_sel = request.GET.get('anio', '')
    try:
        anio_sel = int(anio_sel) if anio_sel else None
    except ValueError:
        anio_sel = None

    if anio_sel:
        balances_filtrados = todos_balances.filter(anio=anio_sel).order_by('mes')
    else:
        balances_filtrados = todos_balances.order_by('anio', 'mes')

    
    balances_chart = list(balances_filtrados)
    labels = [f"{b.get_mes_display()} {b.anio}" for b in balances_chart]
    data_ingresos = [float(b.total_ingresos) for b in balances_chart]
    data_gastos = [float(b.total_gastos) for b in balances_chart]
    data_saldo_final = [float(b.saldo_final) for b in balances_chart]

    
    gastos_cat_total = defaultdict(float)
    ingresos_cat_total = defaultdict(float)
    for b in balances_chart:
        for tx in b.transacciones.all():
            if tx.tipo == 'gasto':
                gastos_cat_total[tx.categoria] += float(tx.monto)
            else:
                ingresos_cat_total[tx.categoria] += float(tx.monto)

    
    gastos_cat_sorted = dict(
        sorted(gastos_cat_total.items(), key=lambda x: x[1], reverse=True)
    )
    ingresos_cat_sorted = dict(
        sorted(ingresos_cat_total.items(), key=lambda x: x[1], reverse=True)
    )

    return render(request, 'finanzas_app/dashboard.html', {
        'balances': balances_filtrados,
        'anios_disponibles': anios_disponibles,
        'anio_sel': anio_sel,
        'labels_json': json.dumps(labels),
        'data_ingresos_json': json.dumps(data_ingresos),
        'data_gastos_json': json.dumps(data_gastos),
        'data_saldo_json': json.dumps(data_saldo_final),
        'gastos_cat_json': json.dumps(gastos_cat_sorted),
        'ingresos_cat_json': json.dumps(ingresos_cat_sorted),
    })


@login_required
def crear_balance(request):
    if request.method == 'POST':
        form = BalanceForm(request.POST, usuario=request.user)
        if form.is_valid():
            balance = form.save(commit=False)
            balance.usuario = request.user
            balance.saldo_inicial = 0
            balance.save()
            messages.success(request, f'Balance {balance} creado.')
            return redirect('finanzas:detalle', pk=balance.pk)
    else:
        hoy = datetime.date.today()
        form = BalanceForm(
            initial={'mes': hoy.month, 'anio': hoy.year},
            usuario=request.user,
        )
    return render(request, 'finanzas_app/balance_form.html', {
        'form': form, 'titulo': 'Crear balance'
    })


@login_required
def editar_balance(request, pk):
    balance = get_object_or_404(Balance, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = BalanceForm(request.POST, instance=balance, usuario=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Balance actualizado.')
            return redirect('finanzas:detalle', pk=balance.pk)
    else:
        form = BalanceForm(instance=balance, usuario=request.user)
    return render(request, 'finanzas_app/balance_form.html', {
        'form': form, 'titulo': 'Editar balance', 'balance': balance
    })


@login_required
def eliminar_balance(request, pk):
    balance = get_object_or_404(Balance, pk=pk, usuario=request.user)
    if request.method == 'POST':
        balance.delete()
        messages.success(request, 'Balance eliminado.')
        return redirect('finanzas:dashboard')
    return render(request, 'finanzas_app/balance_confirmar_eliminar.html', {
        'balance': balance
    })


@login_required
def detalle_balance(request, pk):
    balance = get_object_or_404(Balance, pk=pk, usuario=request.user)
    transacciones = balance.transacciones.all()

    
    gastos_cat = defaultdict(float)
    ingresos_cat = defaultdict(float)
    for tx in transacciones:
        if tx.tipo == 'gasto':
            gastos_cat[tx.categoria] += float(tx.monto)
        else:
            ingresos_cat[tx.categoria] += float(tx.monto)

    
    gastos_cat_sorted = dict(
        sorted(gastos_cat.items(), key=lambda x: x[1], reverse=True)
    )
    ingresos_cat_sorted = dict(
        sorted(ingresos_cat.items(), key=lambda x: x[1], reverse=True)
    )

    form_tx = TransaccionForm()
    if request.method == 'POST':
        form_tx = TransaccionForm(request.POST)
        if form_tx.is_valid():
            tx = form_tx.save(commit=False)
            tx.balance = balance
            tx.save()
            messages.success(request, 'Transacción agregada.')
            return redirect('finanzas:detalle', pk=pk)

    return render(request, 'finanzas_app/detalle_balance.html', {
        'balance': balance,
        'transacciones': transacciones,
        'form_tx': form_tx,
        'gastos_cat_json': json.dumps(gastos_cat_sorted),
        'ingresos_cat_json': json.dumps(ingresos_cat_sorted),
    })


@login_required
def eliminar_transaccion(request, pk):
    tx = get_object_or_404(Transaccion, pk=pk, balance__usuario=request.user)
    balance_pk = tx.balance.pk
    tx.delete()
    messages.success(request, 'Transacción eliminada.')
    return redirect('finanzas:detalle', pk=balance_pk)
