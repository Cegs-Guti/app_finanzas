# FinanzasMes – Proyecto base Django

Aplicación de finanzas personales mensuales construida con Django 6 + Bootstrap 5.

## Funcionalidades

- **Simulador sin login**: cualquier usuario puede crear un balance con ingresos/gastos por categoría. Los datos viven en la sesión y se borran al cerrar la pestaña.
- **Guardar simulación**: al iniciar sesión, el usuario puede guardar la simulación como un balance permanente eligiendo mes y año.
- **Dashboard con historial**: lista de balances propios con gráfico de barras comparativo (ingresos vs. gastos vs. saldo final).
- **Detalle de balance**: tabla de transacciones + gráfico de dona por categoría de gasto.
- **CRUD completo**: crear, editar y eliminar balances y transacciones individuales.

## Instalación
```bash
# 1. Crear y activar entorno
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones
python manage.py migrate

# 4. Crear superusuario (opcional, para el admin)
python manage.py createsuperuser

# 5. Levantar servidor
python manage.py runserver
```

Acceder en: http://127.0.0.1:8000/

## Estructura del proyecto

```
finanzas/
├── manage.py
├── requirements.txt
├── misitio/                  ← Configuración del proyecto
│   ├── settings.py
│   └── urls.py
├── core/                     ← App de páginas generales (home, login/logout)
│   ├── views.py
│   ├── urls.py
│   ├── static/core/css/
│   └── templates/
│       ├── core/home.html
│       ├── layouts/base.html
│       ├── includes/{nav,alertas}.html
│       └── registration/login.html
└── finanzas_app/             ← App principal de finanzas
    ├── models.py             ← Balance + Transaccion
    ├── forms.py              ← BalanceForm, TransaccionForm, SimuladorForms
    ├── views.py              ← Simulador (sesión) + CRUD de balances
    ├── urls.py
    └── templates/finanzas_app/
        ├── simulador.html
        ├── simulador_guardar.html
        ├── dashboard.html
        ├── detalle_balance.html
        ├── balance_form.html
        └── balance_confirmar_eliminar.html
```

## Categorías configurables

En `misitio/settings.py` puedes ajustar las listas `CATEGORIAS_INGRESOS` y `CATEGORIAS_GASTOS`.

## Próximos pasos sugeridos

- Registro de usuarios (`django.contrib.auth` ya incluye las vistas).
- Exportar balance a PDF/Excel.
- Filtros por año en el dashboard.
- Soporte multi-moneda.
