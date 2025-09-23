import paho.mqtt.client as mqtt
import time, json
import os

from dotenv import load_dotenv

# Configuración
BROKER = "localhost"#"192.168.1.254"  # o la IP de tu broker
PORT = 1883
TOPIC = "pico/temperatura" #"sensor/temperatura"  # Topic al que te suscribes
USERNAME = None  # Si no requiere autenticación
PASSWORD = None  # Si no requiere autenticación

def mqtt_to_dict(mqtt_msg)->dict:
    try:
        return json.loads(mqtt_msg)
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON: {e}")
        return dict()

# Callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker con código: {rc}")
    # Suscripción al topic
    client.subscribe(TOPIC)
    # client.subscribe(TOPIC2)
    print(f"Suscripto al topic: {TOPIC}")
    # print(f"Suscripto al topic: {TOPIC2}")

# Callback cuando recibe un mensaje
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en [{msg.topic}]: {msg.payload.decode()}")
    datos = mqtt_to_dict(msg.payload.decode())
    mediciones = datos.keys()
    temperatura = datos['temperatura'] if 'temperatura' in mediciones else float('nan')
    
# Configuración del cliente
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Autenticación (si es necesaria)
if USERNAME and PASSWORD:
    client.username_pw_set(USERNAME, PASSWORD)

# Conexión al broker
client.connect(BROKER, PORT, 60)

# Mantener la conexión activa
print("Escuchando mensajes... Presiona Ctrl+C para salir")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Desconectando...")
    client.disconnect()
