#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar las librerías necesarias
pip install -r requirements.txt

# Recopilar archivos estáticos (diseños, CSS)
python manage.py collectstatic --no-input

# Aplicar cualquier cambio en la estructura de la base de datos
python manage.py migrate