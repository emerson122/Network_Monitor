# Network Monitor

Este script es un monitor de red que captura y analiza las conexiones y el tráfico en tiempo real. Aquí tienes los pasos clave de su funcionamiento:

Inicialización: El script configura las variables iniciales para el monitoreo, como estadísticas de conexiones y tráfico, y configura el sistema de logging para registrar eventos.

Recopilación de uso de red: Usando psutil, se obtienen estadísticas generales de la red, como bytes y paquetes enviados y recibidos.

Captura de paquetes: Utiliza scapy para capturar paquetes en tiempo real. Cada paquete capturado se analiza para identificar direcciones IP de origen y destino, registrando el número de veces que cada par de IPs se conecta y actualizando el tamaño de datos transferidos.

Análisis de conexiones activas: Verifica las conexiones de red activas en tiempo real, identificando direcciones IP remotas, puertos y, si es posible, los nombres de host.

Generación de informes: Al finalizar el monitoreo, se generan informes detallados en formato CSV y se imprimen estadísticas en tiempo real y en un formato tabulado para facilitar la visualización.

Ejecución del monitoreo: El script inicia el monitoreo por un tiempo específico o de manera continua, mostrando estadísticas en tiempo real y capturando las conexiones activas y el tráfico hasta que se detenga manualmente o se complete el tiempo.

Para usar el script necesitarás instalar las dependencias:
``` bash

pip install psutil scapy tabulate
```
El script requiere privilegios de administrador en la mayoría de sistemas para capturar paquetes.
Para ejecutarlo:

``` bash
sudo python network_monitor.py
```