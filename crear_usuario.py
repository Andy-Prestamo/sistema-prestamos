import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# DATOS DEL USUARIO (Cambia esto por lo que quieras)
username = 'lucho'
password = '123456' # Pon una clave real aquí

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, '', password)
    print(f"✅ Usuario '{username}' creado con éxito.")
else:
    print(f"ℹ️ El usuario '{username}' ya existe.")