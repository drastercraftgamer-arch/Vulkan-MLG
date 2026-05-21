# core/network_scanner.py - Escáner de red rápido
import subprocess
import re
import socket
import os
import platform  
from concurrent.futures import ThreadPoolExecutor, as_completed

class NetworkScanner:
    """Escáner de red rápido"""
    
    def __init__(self, logger):
        self.logger = logger
        self.os_type = platform.system() 
        self.gateway_ip = self.get_gateway()
        self.local_ip = self.get_local_ip()
    
    def get_gateway(self):
        """Obtener gateway (mejorado)"""
        try:
            if self.os_type == 'Windows':
                # Windows: netstat -rn o ipconfig
                result = subprocess.run(["ipconfig"], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for i, line in enumerate(lines):
                    if "Puerta de enlace predeterminada" in line:
                        ips = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
                        if ips and ips[0] != "0.0.0.0":
                            return ips[0]
                
                # Método alternativo: route print
                result = subprocess.run(["route", "print", "0.0.0.0"], capture_output=True, text=True)
                match = re.search(r'0\.0\.0\.0\s+0\.0\.0\.0\s+(\d+\.\d+\.\d+\.\d+)', result.stdout)
                if match:
                    return match.group(1)
            
            else:  # Linux/Mac
                result = subprocess.run(["ip", "route"], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if "default via" in line:
                        ips = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
                        if ips:
                            return ips[0]
        
        except Exception as e:
            self.logger.log(f"⚠️ Error obteniendo gateway: {e}", "YELLOW")
        
        # Fallback a IP común
        return "192.168.1.1"
    
    def get_local_ip(self):
        """Obtener IP local (mejorado)"""
        try:
            # Conectar a DNS público para obtener IP real
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            # Fallback: obtener hostname
            try:
                hostname = socket.gethostname()
                return socket.gethostbyname(hostname)
            except:
                return "192.168.1.100"
    
    def ping_device(self, ip, timeout=1):
        """Ping a dispositivo con timeout configurable"""
        try:
            param = '-n' if self.os_type == 'Windows' else '-c'
            
            # Kirynota: "En Windows, -w es milisegundos, en Linux -W es segundos"
            if self.os_type == 'Windows':
                result = subprocess.run(
                    ["ping", param, "1", "-w", str(int(timeout * 1000)), ip],
                    capture_output=True,
                    text=True,
                    timeout=timeout + 0.5
                )
                output = result.stdout.lower()
                # Verificar respuestas exitosas
                return "ttl=" in output or "bytes=" in output or "tiempo=" in output
            else:
                result = subprocess.run(
                    ["ping", param, "1", "-W", str(int(timeout)), ip],
                    capture_output=True,
                    text=True,
                    timeout=timeout + 0.5
                )
                return result.returncode == 0
                
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False
    
    def get_hostname(self, ip):
        """Resolver nombre de host (mejorado)"""
        try:
            # Intentar resolución DNS inversa
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname.split('.')[0]
        except:
            # Fallback: intentar con NetBIOS (En Windows)
            if self.os_type == 'Windows':
                try:
                    result = subprocess.run(["nbtstat", "-A", ip], capture_output=True, text=True, timeout=2)
                    match = re.search(r'<00>\s+UNIQUE\s+(\S+)', result.stdout)
                    if match:
                        return match.group(1)
                except:
                    pass
            return None
    
    def scan_network(self, max_ips=50, ping_timeout=1):
        """Escanear red con parámetros configurables"""
        devices = []
        
        try:
            # Obtener red
            parts = self.gateway_ip.split('.')
            network_base = f"{parts[0]}.{parts[1]}.{parts[2]}"
            
            self.logger.log(f"🌐 Escaneando red {network_base}.0/24...", "CYAN")
            self.logger.log(f"📡 Gateway: {self.gateway_ip} | Mi IP: {self.local_ip}", "DIM")
            
            # Generar IPs a escanear de manera inteligente
            my_last = int(self.local_ip.split('.')[-1])
            ips_to_scan = set()
            
            # Siempre incluir el gateway y PC local
            ips_to_scan.add(self.gateway_ip)
            ips_to_scan.add(self.local_ip)
            
            # IPs cercanas (rangos adyacentes)
            for offset in range(-15, 16):
                ip_num = my_last + offset
                if 1 <= ip_num <= 254:
                    ips_to_scan.add(f"{network_base}.{ip_num}")
            
            # IPs comunes en redes domésticas
            common_ips = [1, 2, 5, 10, 20, 50, 100, 150, 200, 250, 254]
            for ip_num in common_ips:
                ips_to_scan.add(f"{network_base}.{ip_num}")
            
            # KiryNota: "Si hay menos de max_ips, añadir aleatorias"
            if len(ips_to_scan) < max_ips:
                import random
                remaining = max_ips - len(ips_to_scan)
                candidates = [i for i in range(1, 255) if f"{network_base}.{i}" not in ips_to_scan]
                random.shuffle(candidates)
                for i in candidates[:remaining]:
                    ips_to_scan.add(f"{network_base}.{i}")
            
            ips_to_scan = list(ips_to_scan)[:max_ips]
            self.logger.log(f"🔍 Escaneando {len(ips_to_scan)} dispositivos...", "GRAY")
            
            # Escaneo paralelo con barra de progreso
            found_ips = []
            completed = 0
            
            with ThreadPoolExecutor(max_workers=30) as executor:
                futures = {executor.submit(self.ping_device, ip, ping_timeout): ip for ip in ips_to_scan}
                
                for future in as_completed(futures):
                    completed += 1
                    ip = futures[future]
                    
                    if future.result():
                        found_ips.append(ip)
                        self.logger.log(f"  ✓ {ip} - ONLINE", "GREEN")
                    
                    # Mostrar progreso cada 10 IPs
                    if completed % 10 == 0 or completed == len(ips_to_scan):
                        self.logger.log(f"  Progreso: {completed}/{len(ips_to_scan)}", "DIM")
            
            # Crear lista de dispositivos 
            for ip in found_ips:
                # Determinar tipo de dispositivo
                if ip == self.local_ip:
                    name = "⭐ MI PC"
                    device_type = "💻 PC Local"
                elif ip == self.gateway_ip:
                    name = "🌐 ROUTER"
                    device_type = "📡 Gateway"
                else:
                    # Intentar obtener hostname real
                    hostname = self.get_hostname(ip)
                    if hostname:
                        name = f"💻 {hostname}"
                        device_type = "🖥️ PC/Server"
                    else:
                        # Detectar posible Android por puerto 5555
                        is_android = self.check_adb_port(ip)
                        if is_android:
                            name = f"📱 Android Device"
                            device_type = "📱 Android"
                        else:
                            name = f"🔌 Device ({ip.split('.')[-1]})"
                            device_type = "📡 Desconocido"
                
                devices.append({
                    'ip': ip,
                    'mac': 'N/A', 
                    'name': name,
                    'latency': '<10ms',
                    'type': device_type
                })
            
            self.logger.log(f"✅ Escaneo completado: {len(devices)} dispositivos encontrados", "GREEN")
            return devices
            
        except Exception as e:
            self.logger.log(f"❌ Error en escaneo: {e}", "RED")
            return devices
    
    def check_adb_port(self, ip, port=5555):
        """Verificar si el puerto ADB está abierto"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def quick_scan(self):
        """Escaneo rápido (solo IPs comunes)"""
        return self.scan_network(max_ips=20, ping_timeout=0.8)
    
    def full_scan(self):
        """Escaneo completo (toda la red)"""
        return self.scan_network(max_ips=254, ping_timeout=1.5)