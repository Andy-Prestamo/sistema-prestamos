from django import forms
from .models import Cliente, Prestamo, Pago

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'dni', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}),
        }

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        # HEMOS QUITADO 'fecha_inicio' DE AQUÍ:
        fields = ['cliente', 'monto', 'tipo_cuota'] 
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 100'}),
            'tipo_cuota': forms.Select(attrs={'class': 'form-control'}),
            # Ya no necesitamos el widget de fecha_inicio aquí
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['prestamo', 'monto_pagado']
        widgets = {
            'prestamo': forms.Select(attrs={'class': 'form-control'}),
            'monto_pagado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto a cobrar'}),
        }