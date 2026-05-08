import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

def crear_usuarios():
    # Crear admin principal
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Usuario 'admin' creado con éxito.")
    
    # Crear tu usuario personalizado
    if not User.objects.filter(username='andyadmin').exists():
        User.objects.create_user('andyadmin', 'andy@example.com', 'andy123')
        print("Usuario 'andyadmin' creado con éxito.")

if __name__ == '__main__':
    crear_usuarios()