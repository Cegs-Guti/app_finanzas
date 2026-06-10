from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    
    path('simulador/', views.simulador, name='simulador'),
    path('simulador/eliminar/<int:idx>/', views.simulador_eliminar_tx, name='sim_eliminar_tx'),
    path('simulador/limpiar/', views.simulador_limpiar, name='sim_limpiar'),
    path('simulador/guardar/', views.simulador_guardar, name='sim_guardar'),

    
    path('', views.dashboard, name='dashboard'),

    
    path('crear/', views.crear_balance, name='crear_balance'),
    path('crear/nuevo/', views.crear_balance, name='balance_crear'),

    
    path('<int:pk>/', views.detalle_balance, name='detalle'),
    path('<int:pk>/ver/', views.detalle_balance, name='balance_detalle'),

    
    path('<int:pk>/editar/', views.editar_balance, name='editar_balance'),
    path('<int:pk>/editar2/', views.editar_balance, name='balance_editar'),

    
    path('<int:pk>/eliminar/', views.eliminar_balance, name='eliminar_balance'),
    path('<int:pk>/eliminar2/', views.eliminar_balance, name='balance_eliminar'),

    
    path('transaccion/<int:pk>/eliminar/', views.eliminar_transaccion, name='eliminar_tx'),
]
