"""
WSGI config for ErgoProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ErgoProject.settings')
# Importa e inicia el cliente MQTT
from mqttApp.mqtt_client import start_mqtt_client  # Asegúrate de ajustar esta ruta si es diferente
start_mqtt_client()

# Inicializa la aplicación WSGI
application = get_wsgi_application()