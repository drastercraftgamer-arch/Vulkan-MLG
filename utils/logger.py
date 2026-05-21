# utils/logger.py - Sistema de logs
from datetime import datetime

class Logger:
    """Sistema de logging"""
    
    def __init__(self):
        self.log_widget = None
    
    def set_widget(self, widget):
        """Configurar widget de texto"""
        self.log_widget = widget
    
    def log(self, message, color="CYAN"):
        """Escribir log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        print(formatted)
        
        if self.log_widget:
            self.log_widget.insert("end", formatted + "\n")
            self.log_widget.see("end")