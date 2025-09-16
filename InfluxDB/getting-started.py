import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import random
from time import sleep

bucket = "embebidos"
org = "SistemasEmbebidos"
token = "iGnFUOZlqsDGGDuAQuy41ffCMU0j58sa-Pa8cc29aIu9QJN9FBAmnbLrFNmSE3lvK6tCWWA4ehD5vE4UTp2yoA=="
# Store the URL of your InfluxDB instance
url="http://192.168.1.254:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)
temp_b = 25.3

for i in range(50):
    temp = temp_b + random.random()
    print(f'Enviando temperatura {temp}')
    p = influxdb_client.Point("medicion_temp").tag("alumno", "ruben").field("temperatura", temp)
    write_api.write(bucket=bucket, org=org, record=p)
    sleep(30)