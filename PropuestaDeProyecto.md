# Sistema de Wardriving con Visualización en Tiempo Real
## Objetivos
1. Implementar sistema de Wardriving utilizando una tarjeta de desarrollo Raspberry Pi Pico y el módulo GPS NEO-6M.
- El sistema realizará el escaneo de las redes WI-FI disponibles en la zona identificando:
    1. SSID.
    2. Niveles de señal.
    3. Dirección MAC.
    4. Tipo de seguridad (abierta, WEP, WPA-PSK, WPA2-PSK).
- El sistema de wardriving debe conectarse a una red disponible móvil propia (por ejemplo red celular) para obtener acceso a internet.
- Si el sistema cuenta con acceso a internet, enviar la información recabada (por ejemplo cada 2 minutos) mediante MQTT a la plataforma Adafruit IO.
- Si el sistema no cuenta con salida a internet, debe de tener la capacidad de seguir funcionando y guardar la información recabada en una estructura o archivo de texto.
- Cuando el dispositivo logre tener acceso a internet, que realice un vacio de la información a la plataforma Adafruit IO.
- IMPORTANTE: Verificar información GPS. Si no se cuenta con información GPS (por ejemplo el módulo no logra conectarse a algún satelite), el sistema quede en espera del módulo GPS.

2. Desarrollar una interfaz visual para la visualización de la información en un mapa.
Sugerencias:
- Puede implementarse una aplicación web (OpenStreetMap + Leaflet.js o Folium + Python) para visualizar las redes WI-FI identificadas, mostrando la seguridad y niveles de señal.
- La información debe ser recabada desde la plataforma Adafruit IO:
    - A través de HTTP Requests.
    - MQTT

3. Analizar patrones de distribución de redes WI-FI inseguras (Abiertas y WEP) en función de su posición geográfica (latitud/longitud) utilizando algún algoritmo ML de clusterización(DBSCAN o K-Means).

4. Realizar pruebas con al menos tres sistemas independientes (Pruebas entre tres equipos).

## Consideraciones:
- Equipos de máximo 5 personas.
- Tomar en cuenta el número máximo de solicitudes MQTT diarias en la plataforma Adafruit IO.
- Debe de ajustarse las coordenadas UTM a geográficas.
- Código de calidad: Manejo de errores.
- Crear un repositorio en Github para el proyecto.

IMPORTANTE:
El uso de la información recabada puede ser sensible por lo que debe manejarse y utilizarse con responsabilidad.
