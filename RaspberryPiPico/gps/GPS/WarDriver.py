from machine import UART, Pin
from time import sleep, ticks_ms
from micropyGPS import MicropyGPS
import network
import binascii

from umqtt.simple import MQTTClient

SECURITY = {
    0: "Open", 
    1: "WEP", 
    3: "WPA-PSK", 
    5: "WPA2-PSK", 
    7: "WPA/WPA2-PSK"
}

class Wardriver:
    def __init__(self, display=False) -> None:
        self.my_gps = MicropyGPS()
        self.gps_serial = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
        self.display_serial = None
        
        if display:
            self.display_serial = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
        self.last_display_update = 0
        self.display_update_interval = 5000

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.SSID = "SSID"
        self.PASSWORD = "PASSWD"
        self.wifi_networks = None
        self.wifi_file = "wifi_networks.txt"

        self.BROKER = "io.adafruit.com"
        self.PORT = 1883 #8883 #1883
        self.MQTT_CLIENT_ID = "pico-client"
        self.MQTT_USERNAME = "ADAFRUIT_IO_USERNAME"
        self.MQTT_PASSWORD = "ADAFRUIT_IO_API_KEY"
        self.MQTT_TOPIC = f"{self.MQTT_USERNAME}/feeds/sistemasembebidos"
        self.mqtt_client = None

    def __del__(self):
        if self.mqtt_client is not None:
            self.mqtt_client.disconnect()

    def connect_mqtt(self):
        print(f'Conectando al broker {self.BROKER}')
        self.mqtt_client = MQTTClient(client_id=self.MQTT_CLIENT_ID, server=self.BROKER,
                                      port=self.PORT, user=self.MQTT_USERNAME, password=self.MQTT_PASSWORD)
        self.mqtt_client.set_callback(self.mqtt_receive)
        self.mqtt_client.connect()
        print('Conectado al broker MQTT')
        self.mqtt_client.subscribe(self.MQTT_TOPIC)
        print(f'Suscrito al {self.MQTT_TOPIC}')
        
    def mqtt_receive(self, topic, msg):
        print("Mensaje recibido:", topic, msg)

    def mqtt_send(self, message:str):
        if self.mqtt_client is not None:
            message_code = bytearray(message.encode('utf-8'))
            self.mqtt_client.publish(self.MQTT_TOPIC, message_code)

    def send_wifi_ntw(self):
        if self.wifi_networks is not None:
            latitude = str(self.my_gps._latitude[0])
            longitude = str(round(self.my_gps._longitude[1],3))
            for net in self.wifi_networks:
                auth_mode = SECURITY[net[4]]
                self.mqtt_send(f"{net[0].decode()} {auth_mode} {latitude}° {longitude}'\r\n")

    def read_gps(self):
        while self.gps_serial.any():
            data = self.gps_serial.read()
            if data is not None:
                for byte in data:
                    self.my_gps.update(chr(byte))

    def update_display(self):
        current_time = ticks_ms()
        if current_time - self.last_display_update >= self.display_update_interval:
            if self.my_gps.latitude_string() != "0.0" and self.display_serial is not None:
                latitude = str(self.my_gps._latitude[0])
                longitude = str(round(self.my_gps._longitude[1],3))

                lat_d = f'latitude.txt="{self.my_gps._latitude[0]}'.encode('iso-8859-1')
                lat_m = f'{round(self.my_gps._latitude[1],1)} {self.my_gps._latitude[2]}'.encode('iso-8859-1')
                lon_d = f'longitude.txt="{self.my_gps._longitude[0]}'.encode('iso-8859-1')
                lon_m = f'{round(self.my_gps._longitude[1],1)} {self.my_gps._longitude[2]}'.encode('iso-8859-1')

                self.display_serial.write(lat_d)
                self.display_serial.write(b'\xb0')
                self.display_serial.write(lat_m)
                self.display_serial.write('"'.encode('iso-8859-1'))
                self.display_serial.write(b'\xFF\xFF\xFF')

                print(f'{lat_d} {lat_m}')

                sleep(0.1)

                self.display_serial.write(lon_d)
                self.display_serial.write(b'\xb0')
                self.display_serial.write(lon_m)
                self.display_serial.write('"'.encode('iso-8859-1'))
                self.display_serial.write(b'\xFF\xFF\xFF')

                #print(f'{lon_d} {lon_m}')
                if self.wifi_networks is not None and len(self.wifi_networks) > 0:
                    wifi_str = f'wifi.txt="'
                    wifi_text = ""
                    for net in self.wifi_networks:
                        auth_mode = SECURITY[net[4]]
                        print(f'{net[0].decode()} {binascii.hexlify(net[1]).decode()} {net[2]} {str(net[3])} {auth_mode} {str(net[5])}')    
                        wifi_str = wifi_str + f'{net[0].decode()} {auth_mode}\r\n'
                        wifi_text = wifi_text + f"{net[0].decode()} {auth_mode} {latitude}° {longitude}'\r\n"


                    wifi_str = wifi_str + '"'
                    with open(self.wifi_file, 'a') as file:
                        file.write(wifi_text)

            self.last_display_update = current_time

    def connect_wifi(self):
        if not self.wlan.isconnected():
            print("Conectando a WiFi...")
            self.wlan.connect(self.SSID, self.PASSWORD)
            print(f'Conectando a {self.SSID} {self.PASSWORD}')
            while not self.wlan.isconnected():
                sleep(0.5)
        print("Conectado a Wi-Fi:", self.wlan.ifconfig())

    def scan_wifi(self):
        self.wifi_networks = self.wlan.scan()
        if len(self.wifi_networks) > 0:
            latitude = str(self.my_gps._latitude[0])
            longitude = str(round(self.my_gps._longitude[1],3))
            wifi_text = ""
            for net in self.wifi_networks:
                auth_mode = SECURITY[net[4]]
                print(f'{net[0].decode()} {binascii.hexlify(net[1]).decode()} {net[2]} {str(net[3])} {auth_mode} {str(net[5])}')
                wifi_text = wifi_text + f"{net[0].decode()} {auth_mode} {latitude}° {longitude}'\r\n"
            with open(self.wifi_file, 'a') as file:
                file.write(wifi_text)


if __name__ == '__main__':
    try:
        wr = Wardriver(True)
        wr.connect_wifi()
        wr.connect_mqtt()
        print('Arrancando loop principal')
        while True:
            wr.read_gps()
            wr.scan_wifi()
            wr.update_display()
            wr.send_wifi_ntw()
            sleep(10)

    except Exception as e:
        print(f'Hubo un error: {e}')