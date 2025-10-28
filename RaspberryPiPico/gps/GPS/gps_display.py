from machine import UART, Pin
from time import sleep, ticks_ms
from micropyGPS import MicropyGPS

my_gps = MicropyGPS()
gps_serial = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
display_serial = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

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

                lat_d = f'latitude.txt="{my_gps._latitude[0]}'.encode('iso-8859-1')
                lat_m = f'{round(my_gps._latitude[1],1)} {my_gps._latitude[2]}'.encode('iso-8859-1')
                lon_d = f'longitude.txt="{my_gps._longitude[0]}'.encode('iso-8859-1')
                lon_m = f'{round(my_gps._longitude[1],1)} {my_gps._longitude[2]}'.encode('iso-8859-1')

                display_serial.write(lat_d)
                display_serial.write(b'\xb0')
                display_serial.write(lat_m)
                display_serial.write('"'.encode('iso-8859-1'))
                display_serial.write(b'\xFF\xFF\xFF')

                print(f'{lat_d} {lat_m}')

                sleep(0.1)

                display_serial.write(lon_d)
                display_serial.write(b'\xb0')
                display_serial.write(lon_m)
                display_serial.write('"'.encode('iso-8859-1'))
                display_serial.write(b'\xFF\xFF\xFF')

                print(f'{lon_d} {lon_m}')

            last_display_update = current_time
        
        sleep(0.1)
            
    except Exception as e:
        print(f"Error: {e}")
        sleep(1)