FinanzasMes – Proyecto base Django


- **Simulador sin login**: cualquier usuario puede crear un balance con ingresos/gastos por categoría. Los datos viven en la sesión y se borran al cerrar la pestaña.
- **Guardar simulación**: al iniciar sesión, el usuario puede guardar la simulación como un balance permanente eligiendo mes y año.
- **Dashboard con historial**: lista de balances propios con gráfico de barras comparativo (ingresos vs. gastos vs. saldo final).
- **Detalle de balance**: tabla de transacciones + gráfico de dona por categoría de gasto.
- **CRUD completo**: crear, editar y eliminar balances y transacciones individuales.

## Instalación
```bash
# 1. Crear y activar entorno
python -m venv venv       
venv\Scripts\activate           

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones
python manage.py migrate

# 4. Crear superusuario (opcional, para el admin)
python manage.py createsuperuser

# 5. Levantar servidor
python manage.py runserver
```
