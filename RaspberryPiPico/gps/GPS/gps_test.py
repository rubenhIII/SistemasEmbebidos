import machine
from time import sleep



gps = machine.UART(1, baudrate=9600, tx=4, rx=5)

try:
    while True:
        if gps.any():
            line = gps.readline()
            if line:
                line = line.decode('utf-8')
                print(line.strip())
        sleep(2)
except KeyboardInterrupt as e:
    print('Finalizando lecturas desde el gps')