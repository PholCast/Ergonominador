# apps.py
from django.apps import AppConfig

class MqttappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqttApp'
    

    # def ready(self):
    #     # Importa el cliente MQTT y ejecuta el hilo cuando Django inicia
    #     from .mqtt_client import start_mqtt_client
    #     start_mqtt_client()  # Llama a la función para iniciar el cliente MQTT
