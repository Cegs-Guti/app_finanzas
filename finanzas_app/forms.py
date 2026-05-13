from django import forms
from django.conf import settings
from .models import Balance, Transaccion, MESES
import datetime


class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['mes', 'anio', 'saldo_inicial']
        widgets = {
            'anio': forms.NumberInput(attrs={
                'min': 2000,
                'max': 2100,
                'placeholder': datetime.date.today().year,
            }),
            'saldo_inicial': forms.NumberInput(attrs={
                'min': 0,
                'step': '0.01',
                'placeholder': '0.00',
            }),
        }
        labels = {
            'mes': 'Mes',
            'anio': 'Año',
            'saldo_inicial': 'Saldo inicial ($)',
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    def clean(self):
        cleaned = super().clean()
        mes = cleaned.get('mes')
        anio = cleaned.get('anio')
        if mes and anio and self.usuario:
            qs = Balance.objects.filter(usuario=self.usuario, mes=mes, anio=anio)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    f'Ya tienes un balance para ese mes y año.'
                )
        return cleaned


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'categoria', 'descripcion', 'monto']
        widgets = {
            'monto': forms.NumberInput(attrs={'min': 0.01, 'step': '0.01'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripción opcional'}),
        }
        labels = {
            'tipo': 'Tipo',
            'categoria': 'Categoría',
            'descripcion': 'Descripción',
            'monto': 'Monto ($)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categorias_ingresos = [(c, c) for c in settings.CATEGORIAS_INGRESOS]
        categorias_gastos = [(c, c) for c in settings.CATEGORIAS_GASTOS]
        self.fields['categoria'] = forms.ChoiceField(
            choices=[
                ('Ingresos', categorias_ingresos),
                ('Gastos', categorias_gastos),
            ],
            label='Categoría',
        )


# ── Formulario para el simulador anónimo (sin modelo) ──────────────────────

class SimuladorTransaccionForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')],
        label='Tipo',
    )
    categoria = forms.ChoiceField(label='Categoría')
    descripcion = forms.CharField(
        max_length=300, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Descripción opcional'}),
        label='Descripción',
    )
    monto = forms.DecimalField(
        min_value=0.01, decimal_places=2,
        widget=forms.NumberInput(attrs={'min': 0.01, 'step': '0.01'}),
        label='Monto ($)',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categorias_ingresos = [(c, c) for c in settings.CATEGORIAS_INGRESOS]
        categorias_gastos = [(c, c) for c in settings.CATEGORIAS_GASTOS]
        self.fields['categoria'] = forms.ChoiceField(
            choices=[
                ('Ingresos', categorias_ingresos),
                ('Gastos', categorias_gastos),
            ],
            label='Categoría',
        )


class SimuladorInicioForm(forms.Form):
    saldo_inicial = forms.DecimalField(
        min_value=0, decimal_places=2, initial=0,
        widget=forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'placeholder': '0.00'}),
        label='Saldo inicial ($)',
    )
