import paho.mqtt.client as paho
from paho import mqtt
import threading
import json  # Usaremos JSON si el mensaje viene en formato JSON
from django.utils import timezone
from mqttApp.models import SensorLuz, SensorSonido, SensorTemp  # Importamos el modelo

# Variable global para el hilo
mqtt_thread = None

# Callback para conexión
def on_connect(client, userdata, flags, rc, properties=None):
    print("Conectado con código %s." % rc)

# Callback para publicaciones exitosas
def on_publish(client, userdata, mid, properties=None):
    print("Mensaje publicado con mid: " + str(mid))

# Callback para suscripciones
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Suscrito al tópico con mid: " + str(mid) + " QoS: " + str(granted_qos))

def on_message(client, userdata, message):
    # Aquí asumo que el mensaje es un JSON que incluye el sensor_id y el value
    value = message.payload.decode()
    print("valor enviado :", value)
    # Usamos match para decidir en qué tabla guardar según el sensor_id
    match message.topic:
        case "sensors/temp":
            SensorTemp.objects.create(value=value, date=timezone.now())
        case "sensors/sonido":
            SensorSonido.objects.create(value=value, date=timezone.now())
        case "sensors/luz":
            SensorLuz.objects.create(value=value, date=timezone.now())
        case _:
            print(f"topic no se encontró o algo así ")

def start_mqtt_client():
    global mqtt_thread
    if mqtt_thread is not None and mqtt_thread.is_alive():
        print("El cliente MQTT ya está en ejecución.")
        return  # No iniciar un nuevo hilo si ya está en ejecución

    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    # Configura TLS para conexión segura
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("LeoPol", "leopolleopol")

    # Conecta al broker de HiveMQ
    client.connect("0ef00983738c44e2880d6f556d2fb494.s1.eu.hivemq.cloud", 8883)

    # Suscríbete a un tópico
    client.subscribe("sensors/#", qos=1)

    # Publica un mensaje de prueba
    #client.publish("encyclopedia/temperature", payload='{ "sensor_id": "sensor1", "value": 24.5 }', qos=1)

    # Inicia el bucle de espera de mensajes en segundo plano
    client.loop_forever()

    mqtt_thread = threading.current_thread()  # Asigna el hilo actual
