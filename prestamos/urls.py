from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.clientes, name='clientes'),
    path('prestamos/', views.prestamos_lista, name='prestamos'),
    path('pagos/', views.pagos, name='pagos'),
]