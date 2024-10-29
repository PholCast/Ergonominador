import paho.mqtt.client as paho
from paho import mqtt
import threading
import json  # Usaremos JSON si el mensaje viene en formato JSON
from django.utils import timezone
from mqttApp.models import SensorLuz, SensorSonido, SensorTemp, Alert  # Importamos el modelo

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
        case "alert/distancia":
            Alert.objects.create(type_alert="Distancia", message=f"Distancia a la pantalla es muy baja: {value} cm")
        case "alert/temp":
            Alert.objects.create(type_alert="Temperatura", message=f"Alerta de Temperatura : {value} grados")
        case "alert/luz":
            Alert.objects.create(type_alert="Luz", message=f"Alerta de Luz : {value} lux")
        case "alert/postura":
            Alert.objects.create(type_alert="Postura", message=f"Alerta de Postura : {value} si")
        case _:
            print(f"topic no se encontró o algo así")

# Función que ejecutará el loop del cliente MQTT en un hilo separado
def mqtt_loop(client):
    client.loop_forever()

def start_mqtt_client():
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

    # Suscríbete a los tópicos
    client.subscribe("sensors/#", qos=1)
    client.subscribe("alert/#", qos=1)

    # Inicia el loop en un hilo separado
    mqtt_thread = threading.Thread(target=mqtt_loop, args=(client,))
    mqtt_thread.daemon = True  # Esto permite que el hilo se cierre al terminar el servidor
    mqtt_thread.start()