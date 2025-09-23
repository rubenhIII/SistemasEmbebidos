import dht
import machine
import time

global temp
global hum

d = dht.DHT11(machine.Pin(4))

while(True):
    time.sleep(2)
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    print(f"Temperatura: {temp}")
    print(f"Humedad: {hum}")