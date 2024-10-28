import psutil
import time
from datetime import datetime  # Importación corregida
import socket
import logging
import csv
from scapy.all import *
from collections import defaultdict
from tabulate import tabulate

class NetworkMonitor:
    def __init__(self):
        self.connections = defaultdict(int)
        self.traffic_stats = defaultdict(lambda: {'bytes_sent': 0, 'bytes_recv': 0})
        self.start_time = datetime.now()  # Uso corregido de datetime
        
        # Configuración del logging
        logging.basicConfig(
            filename='network_monitor.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def get_network_usage(self):
        """Obtiene estadísticas de uso de red actuales"""
        return psutil.net_io_counters()
    
    def capture_packet(self, packet):
        """Callback para procesar paquetes capturados"""
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            self.connections[(src_ip, dst_ip)] += 1
            
            # Actualizar estadísticas de tráfico
            size = len(packet)
            self.traffic_stats[src_ip]['bytes_sent'] += size
            self.traffic_stats[dst_ip]['bytes_recv'] += size
    
    def generate_report(self):
        """Genera un informe detallado del monitoreo"""
        current_time = datetime.now()  # Uso corregido de datetime
        duration = current_time - self.start_time
        
        # Estadísticas generales
        net_stats = self.get_network_usage()
        
        # Preparar datos para el informe
        report = [
            ["Tiempo de monitoreo", str(duration)],
            ["Bytes enviados", f"{net_stats.bytes_sent:,}"],
            ["Bytes recibidos", f"{net_stats.bytes_recv:,}"],
            ["Paquetes enviados", f"{net_stats.packets_sent:,}"],
            ["Paquetes recibidos", f"{net_stats.packets_recv:,}"]
        ]
        
        # Guardar reporte en CSV
        with open(f'network_report_{current_time.strftime("%Y%m%d_%H%M%S")}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Métrica", "Valor"])
            writer.writerows(report)
        
        return tabulate(report, headers=["Métrica", "Valor"], tablefmt="grid")
    
    def analyze_connections(self):
        """Analiza las conexiones activas"""
        active_connections = []
        
        for conn in psutil.net_connections():
            if conn.status == 'ESTABLISHED':
                try:
                    hostname = socket.gethostbyaddr(conn.raddr.ip)[0]
                except:
                    hostname = "Desconocido"
                
                active_connections.append({
                    'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                    'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}",
                    'hostname': hostname,
                    'pid': conn.pid
                })
        
        return active_connections
    
    def start_monitoring(self, duration_seconds=None):
        """Inicia el monitoreo de red"""
        print("Iniciando monitoreo de red...")
        logging.info("Monitoreo iniciado")
        
        try:
            # Iniciar captura de paquetes en segundo plano
            sniff_thread = AsyncSniffer(prn=self.capture_packet, store=0)
            sniff_thread.start()
            
            start_time = time.time()
            while True:
                if duration_seconds and time.time() - start_time > duration_seconds:
                    break
                
                # Mostrar estadísticas en tiempo real
                stats = self.get_network_usage()
                active_conns = len(self.analyze_connections())
                
                print("\n" + "="*50)
                print(f"Estadísticas actuales ({datetime.now().strftime('%H:%M:%S')})")  # Uso corregido de datetime
                print(f"Conexiones activas: {active_conns}")
                print(f"Bytes enviados: {stats.bytes_sent:,}")
                print(f"Bytes recibidos: {stats.bytes_recv:,}")
                print("="*50)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nDeteniendo monitoreo...")
        finally:
            sniff_thread.stop()
            print("\nGenerando informe final...")
            print(self.generate_report())
            logging.info("Monitoreo finalizado")

if __name__ == "__main__":
    monitor = NetworkMonitor()
    # Monitorear durante 60 segundos (puedes ajustar este valor o eliminar el parámetro para monitoreo continuo)
    monitor.start_monitoring(duration_seconds=60)