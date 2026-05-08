from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/historial/<int:pk>/', views.historial_cliente, name='historial_cliente'),
    path('prestamos/nuevo/', views.crear_prestamo, name='crear_prestamo'),
    path('pagos/registrar/', views.registrar_pago, name='registrar_pago'),
]