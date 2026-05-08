#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Esta línea crea el usuario automáticamente usando el otro archivo que creaste
python crear_usuario.py