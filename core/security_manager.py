# core/security_manager.py - Gestor de seguridad
import hashlib
import getpass
import os
from datetime import datetime

class SecurityManager:
    """Gestor de seguridad para operaciones críticas"""
    
    def __init__(self, logger):
        self.logger = logger
        self.operation_log = []
        self.safe_mode = True
    
    def require_confirmation(self, action, target, severity="medium"):
        """Requerir confirmación para acciones peligrosas"""
        severity_levels = {
            "low": ["abrir", "ver", "listar", "explorar"],
            "medium": ["bloquear", "desbloquear", "notificar", "grabar"],
            "high": ["borrar", "eliminar", "wipe", "formatear", "instalar"],
            "critical": ["root", "bootloader", "recovery", "flash"]
        }
        
        # Verificar si es acción peligrosa
        action_lower = action.lower()
        is_dangerous = any(level in action_lower for level in severity_levels["high"] + severity_levels["critical"])
        
        if is_dangerous and self.safe_mode:
            self.logger.log(f"⚠️ OPERACIÓN SENSIBLE: {action} en {target}", "YELLOW")
            response = input(f"¿Confirmas '{action}' en {target}? (sí/no): ")
            return response.lower() == 'sí' or response.lower() == 'si'
        
        return True
    
    def log_operation(self, operation, target, result):
        """Registrar operación para auditoría"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'target': target,
            'result': result
        }
        self.operation_log.append(log_entry)
        
        # Guardar a archivo si es crítica
        if 'block' in operation.lower() or 'wipe' in operation.lower():
            with open('operations.log', 'a') as f:
                f.write(f"{log_entry['timestamp']} - {operation} - {target} - {result}\n")
    
    def get_operation_history(self, limit=50):
        """Obtener historial de operaciones"""
        return self.operation_log[-limit:]