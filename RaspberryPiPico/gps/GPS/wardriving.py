from machine import UART, Pin
from time import sleep, ticks_ms
from micropyGPS import MicropyGPS
import network
import binascii
import os

security = {
    0: "Open", 
    1: "WEP", 
    3: "WPA-PSK", 
    5: "WPA2-PSK", 
    7: "WPA/WPA2-PSK"
}

latitude = ""
longitude = ""
wifi_file = "wifi_networks.txt"

def scan_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #(ssid, bssid, channel, RSSI, security, hidden) = wlan.scan()
    return wlan.scan()

my_gps = MicropyGPS()
gps_serial = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

last_display_update = 0
display_update_interval = 5000

while True:
    try:
        # Leer GPS continuamente
        while gps_serial.any():
            data = gps_serial.read()
            if data is not None:
                for byte in data:
                    my_gps.update(chr(byte))
        
        # Actualizar display cada 5 segundos
        current_time = ticks_ms()
        if current_time - last_display_update >= display_update_interval:
            if my_gps.latitude_string() != "0.0":

                latitude = str(my_gps._latitude[0])
                longitude = str(round(my_gps._longitude[1],3))

            last_display_update = current_time

            wifi_networks = scan_wifi()
            if len(wifi_networks) > 0:
                wifi_str = f'wifi.txt="'
                wifi_text = ""
                for net in wifi_networks:
                    auth_mode = security[net[4]]
                    print(f'{net[0].decode()} {binascii.hexlify(net[1]).decode()} {net[2]} {str(net[3])} {auth_mode} {str(net[5])}')    
                    wifi_str = wifi_str + f'{net[0].decode()} {auth_mode}\r\n'
                    wifi_text = wifi_text + f"{net[0].decode()} {auth_mode} {latitude}° {longitude}'\r\n"
                
                wifi_str = wifi_str + '"'
                with open(wifi_file, 'a') as file:
                    file.write(wifi_text)
        sleep(15)
            
    except Exception as e:
        print(f"Error: {e}")
        sleep(1)