import network
import time
from umqtt.simple import MQTTClient
import machine

# Configuración WiFi
SSID = "SistemasEmbebidos"
PASSWORD = "abcde1234"

# Configuración MQTT
MQTT_BROKER = "test.mosquitto.org"   # Puedes usar tu servidor
MQTT_CLIENT_ID = "pico-client"
MQTT_TOPIC = b"pico/test"

# LED integrado (para feedback)
led = machine.Pin("LED", machine.Pin.OUT)

# Conectar a WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Conectado a WiFi:", wlan.ifconfig())

# Callback al recibir mensajes
def sub_cb(topic, msg):
    print("Mensaje recibido:", topic, msg)
    if msg == b"ON":
        led.value(1)
    elif msg == b"OFF":
        led.value(0)

# Programa principal
def main():
    connect_wifi()
    
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.set_callback(sub_cb)
    client.connect()
    print("Conectado al broker MQTT:", MQTT_BROKER)
    
    # Suscribirse a un tópico
    client.subscribe(MQTT_TOPIC)
    
    try:
        while True:
            # Publicar un mensaje
            client.publish(MQTT_TOPIC, b"Hola desde Pico W")
            print("Mensaje publicado")
            
            # Revisar si hay mensajes
            client.check_msg()
            
            time.sleep(5)
    finally:
        client.disconnect()

main()
