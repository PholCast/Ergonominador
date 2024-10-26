from django.apps import AppConfig


class MqttappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqttApp'

    def ready(self):
        # Importa el cliente MQTT y ejecuta el hilo cuando Django inicia
        from . import mqtt_client
