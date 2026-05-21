# utils/config.py - Configuración
import json
import os

class ConfigManager:
    """Gestor de configuración"""
    
    def __init__(self):
        self.config_file = "config.json"
        self.config = self.load()
    
    def load(self):
        """Cargar configuración"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"saved_devices": []}
    
    def save(self):
        """Guardar configuración"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def save_device(self, device):
        """Guardar dispositivo"""
        self.config["saved_devices"].append(device)
        self.save()
    
    def get_saved_devices(self):
        """Obtener dispositivos guardados"""
        return self.config.get("saved_devices", [])