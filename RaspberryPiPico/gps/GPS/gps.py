from machine import UART, Pin
from time import sleep
from micropyGPS import MicropyGPS

my_gps = MicropyGPS()
gps_serial = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

while True:
    try:
        while gps_serial.any():
            data = gps_serial.read()
            for byte in data:
                stat = my_gps.update(chr(byte))
                if stat is not None:
                    # Print parsed GPS data
                    print('UTC Timestamp:', my_gps.timestamp)
                    print('Date:', my_gps.date_string('long'))
                    print('Latitude:', my_gps.latitude_string())
                    print('Longitude:', my_gps.longitude_string())
                    print('Altitude:', my_gps.altitude)
                    print('Satellites in use:', my_gps.satellites_in_use)
                    print('Horizontal Dilution of Precision:', my_gps.hdop)
                    print()
        sleep(1)
            
    except Exception as e:
        print(f"An error occurred: {e}")