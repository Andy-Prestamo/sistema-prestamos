from django.contrib import admin
from django.urls import path
from prestamos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    
    # Clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Préstamos
    path('prestamos/', views.prestamos_lista, name='prestamos_lista'),
    path('prestamos/nuevo/', views.crear_prestamo, name='crear_prestamo'),
    path('prestamos/eliminar/<int:pk>/', views.eliminar_prestamo, name='eliminar_prestamo'),
    
    # Pagos
    path('pagos/registrar/', views.registrar_pago, name='registrar_pago'),
]