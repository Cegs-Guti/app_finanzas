from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    # Simulador (anónimo / autenticado)
    path('simulador/', views.simulador, name='simulador'),
    path('simulador/eliminar/<int:idx>/', views.simulador_eliminar_tx, name='sim_eliminar_tx'),
    path('simulador/limpiar/', views.simulador_limpiar, name='sim_limpiar'),
    path('simulador/guardar/', views.simulador_guardar, name='sim_guardar'),

    # Dashboard y balances (login requerido)
    path('', views.dashboard, name='dashboard'),
    path('crear/', views.crear_balance, name='crear_balance'),
    path('<int:pk>/', views.detalle_balance, name='detalle'),
    path('<int:pk>/editar/', views.editar_balance, name='editar_balance'),
    path('<int:pk>/eliminar/', views.eliminar_balance, name='eliminar_balance'),
    path('transaccion/<int:pk>/eliminar/', views.eliminar_transaccion, name='eliminar_tx'),
]
