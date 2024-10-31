import paho.mqtt.client as paho
from paho import mqtt
import threading
import json  # Usaremos JSON si el mensaje viene en formato JSON
from django.utils import timezone
from mqttApp.models import Postura,SensorLuz, SensorSonido, SensorTemp, Alert  # Importamos el modelo
from datetime import datetime  # Importa datetime

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
    value = float(message.payload.decode())
    print("valor enviado :", value)
    
    
    system_time = datetime.now()  # Obtiene la hora del sistema
    print(system_time)
    # Usamos match para decidir en qué tabla guardar según el sensor_id
    match message.topic:
        case "sensorsPHOLLEO/temp":
            SensorTemp.objects.create(value=value, date=system_time)
            
        case "sensorsPHOLLEO/sonido":
            SensorSonido.objects.create(value=value, date=system_time)
        case "sensorsPHOLLEO/luz":
            SensorLuz.objects.create(value=value, date=system_time)
        case "alertPHOLLEO/distancia":
            Alert.objects.create(created_at=system_time,type_alert="Distancia", message=f"Distancia a la pantalla es muy baja: {value} cm")
        case "alertPHOLLEO/temp":
            if value > 30:
                Alert.objects.create(created_at=system_time,type_alert="Temperatura", message=f"Alerta: la temperatura es muy alta! ( {value} grados )")
            else:
                Alert.objects.create(created_at=system_time,type_alert="Temperatura", message=f"Alerta: la temperatura es muy baja! ( {value} grados )")
        case "alertPHOLLEO/luz":
            if value < 20:
                Alert.objects.create(created_at=system_time,type_alert="Luz", message=f"Alerta: la luz ambiente es muy baja!( {value} lux )")
            else:
                Alert.objects.create(created_at=system_time,type_alert="Luz", message=f"Alerta: la luz ambiente esd muy alta!( {value} lux )")
        case "alertPHOLLEO/postura":
            Postura.objects.create(created_at=system_time,tiempo=value, semaforo=f"{value}")
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
    #client.username_pw_set("LeoPol", "leopolleopol")

    # Conecta al broker de HiveMQ
    client.connect("broker.hivemq.com", 8883)

    # Suscríbete a los tópicos
    client.subscribe("sensorsPHOLLEO/#", qos=1)
    client.subscribe("alertPHOLLEO/#", qos=1)

    # Inicia el loop en un hilo separado
    mqtt_thread = threading.Thread(target=mqtt_loop, args=(client,))
    mqtt_thread.daemon = True  # Esto permite que el hilo se cierre al terminar el servidor
    mqtt_thread.start()