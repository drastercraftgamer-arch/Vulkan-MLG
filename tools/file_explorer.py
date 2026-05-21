# tools/file_explorer.py - Explorador de archivos dual (PC + Android) 
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import subprocess
import threading
import os
import shutil
import re
import platform
from datetime import datetime

# Kirynota: "Algo me dice que no funciona muy bien ptm..."

class FileExplorer: # 
    """Explorador de archivos - Funciona para PC y Android"""
    
    def __init__(self, parent, mode="pc", device_ip=None, device_name=None, log_callback=None):
        self.parent = parent
        self.mode = mode
        self.device_ip = device_ip
        self.device_name = device_name or ("PC Local" if mode == "pc" else "Android")
        self.log = log_callback
        self.os_type = platform.system()
        
        # Inicializar ruta según modo
        if mode == "pc":
            self.current_path = os.path.expanduser("~")  # Carpeta de usuario
        else:
            self.current_path = "/sdcard/"
        
        self.window = None
        self.tree = None
        self.clipboard = None
        self.clipboard_action = None
        self.history = []
        self.history_index = -1
        
        # Colores
        self.colors = {
            'bg': '#1e1e1e',
            'panel': '#2d2d2d',
            'cyan': '#00ffff',
            'green': '#44ff44',
            'yellow': '#ffff44',
            'red': '#ff4444',
        }
    
    def open(self):
        """Abrir ventana"""
        icon = "💻" if self.mode == "pc" else "📱"
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"{icon} Explorador - {self.device_name}")
        self.window.geometry("1200x700")
        self.window.configure(bg=self.colors['bg'])
        self.window.minsize(800, 500)
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """Configurar interfaz"""
        # Toolbar
        toolbar = tk.Frame(self.window, bg=self.colors['panel'], height=40)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        # Botones de navegación
        btn_back = tk.Button(toolbar, text="◀ Atrás", command=self.go_back,
                            bg=self.colors['panel'], fg=self.colors['cyan'],
                            relief=tk.FLAT, cursor="hand2")
        btn_back.pack(side=tk.LEFT, padx=2)
        
        btn_forward = tk.Button(toolbar, text="▶ Adelante", command=self.go_forward,
                               bg=self.colors['panel'], fg=self.colors['cyan'],
                               relief=tk.FLAT, cursor="hand2")
        btn_forward.pack(side=tk.LEFT, padx=2)
        
        tk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Botones principales
        buttons = [
            ("🏠 Inicio", self.go_home),
            ("⬆️ Subir", self.go_up),
            ("🔄 Refrescar", self.refresh),
            ("📁 Nueva carpeta", self.new_folder),
            ("📤 Subir archivo", self.upload_file),
            ("📥 Descargar", self.download_selected),
            ("🗑️ Eliminar", self.delete_selected),
            ("📋 Copiar", self.copy_selected),
            ("✂️ Cortar", self.cut_selected),
            ("📌 Pegar", self.paste_selected),
        ]
        
        for text, cmd in buttons:
            btn = tk.Button(toolbar, text=text, command=cmd,
                           bg=self.colors['panel'], fg=self.colors['cyan'],
                           relief=tk.FLAT, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=2)
        
        # Ruta
        path_frame = tk.Frame(self.window, bg=self.colors['bg'])
        path_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(path_frame, text="📍 Ruta:", bg=self.colors['bg'], fg=self.colors['cyan']).pack(side=tk.LEFT, padx=5)
        
        self.path_entry = tk.Entry(path_frame, bg=self.colors['panel'], fg=self.colors['cyan'],
                                   font=("Consolas", 10), insertbackground=self.colors['cyan'])
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.path_entry.bind('<Return>', lambda e: self.go_to_path())
        
        # Frame principal con Treeview
        main_frame = tk.Frame(self.window, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview con scrollbars
        tree_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("name", "size", "modified", "type")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")
        
        # Configurar columnas
        self.tree.heading("#0", text="Nombre")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("size", text="Tamaño")
        self.tree.heading("modified", text="Modificado")
        self.tree.heading("type", text="Tipo")
        
        self.tree.column("#0", width=450)
        self.tree.column("name", width=0, stretch=False)
        self.tree.column("size", width=100, anchor=tk.E)
        self.tree.column("modified", width=150)
        self.tree.column("type", width=100)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Eventos
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.on_right_click)
        
        # Barra de estado
        self.status_label = tk.Label(self.window, text="✅ Listo", 
                                     bg=self.colors['bg'], fg="#888888", anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
        
        # Atajos de teclado
        self.window.bind('<F5>', lambda e: self.refresh())
        self.window.bind('<BackSpace>', lambda e: self.go_up())
        self.window.bind('<Delete>', lambda e: self.delete_selected())
        self.window.bind('<Control-c>', lambda e: self.copy_selected())
        self.window.bind('<Control-x>', lambda e: self.cut_selected())
        self.window.bind('<Control-v>', lambda e: self.paste_selected())
    
    def add_to_history(self, path):
        """Añadir ruta al historial"""
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        self.history.append(path)
        self.history_index = len(self.history) - 1
    
    def go_back(self):
        """Ir atrás en historial"""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_path = self.history[self.history_index]
            self.refresh()
    
    def go_forward(self):
        """Ir adelante en historial"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_path = self.history[self.history_index]
            self.refresh()
    
    def validate_path(self, path):
        """Validar que el path es seguro"""
        if '..' in path:
            self.status_label.config(text="❌ Path traversal no permitido")
            return False
        
        if self.mode == "android":
            if not path.startswith('/sdcard/'):
                self.status_label.config(text="❌ Solo se permite acceso a /sdcard/")
                return False
        
        if self.mode == "pc":
            forbidden = ['C:\\Windows\\System32', 'C:\\Windows\\System', '/etc', '/boot', '/System', '/usr']
            for forbidden_path in forbidden:
                if path.lower().startswith(forbidden_path.lower()):
                    self.status_label.config(text="❌ Acceso a directorios del sistema denegado")
                    return False
        
        return True
    
    def get_pc_listing(self):
        """Listar archivos del PC - CORREGIDO"""
        items = []
        
        try:
            if not os.path.exists(self.current_path):
                self.status_label.config(text=f"❌ Ruta no existe: {self.current_path}")
                return items
            
            if not os.access(self.current_path, os.R_OK):
                self.status_label.config(text=f"❌ Sin permisos de lectura: {self.current_path}")
                return items
            
            items_list = os.listdir(self.current_path)
            
            for item in items_list:
                full_path = os.path.join(self.current_path, item)
                try:
                    # Ocultar archivos del sistema solo en Linux/Mac
                    if self.os_type != 'Windows' and item.startswith('.'):
                        continue
                    
                    stat = os.stat(full_path)
                    size = stat.st_size
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    
                    if os.path.isdir(full_path):
                        items.append(("📁 " + item, "", modified, "Carpeta"))
                    else:
                        ext = os.path.splitext(item)[1].lower()
                        icon = self.get_icon(ext)
                        size_str = self.format_size(size)
                        items.append((f"{icon} {item}", size_str, modified, ext.upper() if ext else "Archivo"))
                except (PermissionError, OSError):
                    items.append((f"🔒 {item}", "?", modified, "Protegido"))
                    continue
                    
        except Exception as e:
            if self.log:
                self.log(f"Error al listar {self.current_path}: {e}")
            self.status_label.config(text=f"❌ Error: {str(e)[:50]}")
        
        items.sort(key=lambda x: (not x[3].startswith('Carpeta'), x[0].lower()))
        return items
    
    def get_android_listing(self):
        """Listar archivos del Android"""
        items = []
        
        stdout, stderr = self.run_adb_command(f'ls -la "{self.current_path}"')
        
        if not stdout or "No such file" in stderr:
            return items
        
        pattern = re.compile(r'^([drwx-]+)\s+\d+\s+\S+\s+\S+\s+(\d+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s+(.+)$')
        
        for line in stdout.split('\n'):
            line = line.strip()
            if not line or line.startswith('total'):
                continue
            
            if line.endswith('.') or line.endswith('..'):
                continue
            
            match = pattern.match(line)
            if match:
                perms, size, date, name = match.groups()
                name = name.strip()
                name = re.sub(r'\x1b\[[0-9;]*m', '', name)
                
                if name and name not in ['.', '..']:
                    if perms.startswith('d'):
                        items.append(("📁 " + name, "", date, "Carpeta"))
                    else:
                        icon = self.get_icon(os.path.splitext(name)[1])
                        items.append((f"{icon} {name}", self.format_size(int(size)), date, "Archivo"))
        
        items.sort(key=lambda x: (not x[3].startswith('Carpeta'), x[0].lower()))
        return items
    
    def run_adb_command(self, cmd):
        """Ejecutar comando ADB"""
        if not self.device_ip:
            return "", "No device"
        
        full_cmd = f'adb -s {self.device_ip}:5555 shell {cmd}'
        try:
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=15)
            return result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return "", "Timeout"
        except Exception as e:
            return "", str(e)
    
    def refresh(self):
        """Refrescar vista"""
        if not self.validate_path(self.current_path):
            return
        
        self.status_label.config(text="🔄 Cargando...")
        self.window.update_idletasks()
        
        if not self.history or self.history[-1] != self.current_path:
            self.add_to_history(self.current_path)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, self.current_path)
        
        if self.mode == "pc":
            items = self.get_pc_listing()
        else:
            items = self.get_android_listing()
        
        for item in items:
            text = item[0]
            values = item
            tags = ('folder',) if item[3] == "Carpeta" else ('file',)
            self.tree.insert("", tk.END, text=text, values=values, tags=tags)
        
        self.tree.tag_configure('folder', foreground=self.colors['cyan'])
        self.tree.tag_configure('file', foreground=self.colors['green'])
        
        folders_count = sum(1 for i in items if i[3] == "Carpeta")
        files_count = len(items) - folders_count
        self.status_label.config(text=f"✅ {folders_count} carpetas, {files_count} archivos")
    
    def get_icon(self, ext):
        """Obtener icono según extensión"""
        icons = {
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.bmp': '🖼️', '.svg': '🖼️',
            '.mp4': '🎬', '.mkv': '🎬', '.avi': '🎬', '.mov': '🎬', '.wmv': '🎬', '.flv': '🎬',
            '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵', '.aac': '🎵', '.ogg': '🎵',
            '.pdf': '📕', '.apk': '📦', '.exe': '⚙️', '.msi': '⚙️',
            '.doc': '📝', '.docx': '📝', '.txt': '📃', '.rtf': '📃', '.odt': '📃',
            '.zip': '🗜️', '.rar': '🗜️', '.7z': '🗜️', '.tar': '🗜️', '.gz': '🗜️',
            '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨', '.json': '📋',
            '.xls': '📊', '.xlsx': '📊', '.ppt': '📽️', '.pptx': '📽️',
        }
        return icons.get(ext, '📄')
    
    def format_size(self, size):
        """Formatear tamaño"""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size/(1024*1024):.1f} MB"
        else:
            return f"{size/(1024*1024*1024):.2f} GB"
    
    def on_double_click(self, event):
        """Doble clic"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        name = item['text']
        clean_name = name.split(' ', 1)[-1] if ' ' in name and name[0] in '📁📄🖼️🎬🎵📕📦⚙️📝📃🗜️🐍🔒' else name
        
        if name.startswith('📁'):
            if self.mode == "pc":
                new_path = os.path.join(self.current_path, clean_name)
            else:
                new_path = self.current_path.rstrip('/') + '/' + clean_name + '/'
            
            if os.path.exists(new_path) or self.mode == "android":
                self.current_path = new_path
                self.refresh()
        else:
            self.open_file(clean_name)
    
    def open_file(self, filename):
        """Abrir archivo"""
        if self.mode == "pc":
            full_path = os.path.join(self.current_path, filename)
            try:
                os.startfile(full_path)
                self.status_label.config(text=f"✅ Abierto: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir:\n{e}")
                self.status_label.config(text=f"❌ Error al abrir: {filename}")
        else:
            if messagebox.askyesno("Descargar", f"¿Descargar '{filename}' a tu PC?"):
                self.download_file(filename)
    
    def download_file(self, filename):
        """Descargar archivo del Android"""
        if self.mode != "android":
            return
        
        full_path = self.current_path.rstrip('/') + '/' + filename
        save_path = filedialog.asksaveasfilename(
            title="Guardar como",
            initialfile=filename,
            defaultextension=os.path.splitext(filename)[1]
        )
        
        if save_path:
            self.status_label.config(text=f"⬇️ Descargando {filename}...")
            
            cmd = f'adb -s {self.device_ip}:5555 pull "{full_path}" "{save_path}"'
            
            def download():
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        self.window.after(0, lambda: self.status_label.config(text=f"✅ Descargado: {filename}"))
                        self.window.after(0, lambda: self.log(f"✅ Descargado: {filename}"))
                        if messagebox.askyesno("Descarga completada", f"¿Abrir {filename}?"):
                            self.window.after(0, lambda: os.startfile(save_path))
                    else:
                        self.window.after(0, lambda: self.status_label.config(text=f"❌ Error descargando: {filename}"))
                        self.window.after(0, lambda: messagebox.showerror("Error", f"No se pudo descargar:\n{result.stderr}"))
                except Exception as e:
                    self.window.after(0, lambda: self.status_label.config(text=f"❌ Error: {str(e)[:50]}"))
            
            threading.Thread(target=download, daemon=True).start()
    
    def upload_file(self):
        """Subir archivo"""
        file_path = filedialog.askopenfilename(title="Seleccionar archivo para subir")
        if not file_path:
            return
        
        filename = os.path.basename(file_path)
        
        if self.mode == "pc":
            dest = os.path.join(self.current_path, filename)
            try:
                shutil.copy2(file_path, dest)
                self.status_label.config(text=f"✅ Subido: {filename}")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo copiar:\n{e}")
        else:
            self.status_label.config(text=f"⬆️ Subiendo {filename}...")
            dest_path = self.current_path.rstrip('/') + '/' + filename
            cmd = f'adb -s {self.device_ip}:5555 push "{file_path}" "{dest_path}"'
            
            def upload():
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        self.window.after(0, lambda: self.status_label.config(text=f"✅ Subido: {filename}"))
                        self.window.after(0, lambda: self.refresh())
                        self.window.after(0, lambda: self.log(f"✅ Subido a Android: {filename}"))
                    else:
                        self.window.after(0, lambda: self.status_label.config(text=f"❌ Error subiendo: {filename}"))
                except Exception as e:
                    self.window.after(0, lambda: self.status_label.config(text=f"❌ Error: {str(e)[:50]}"))
            
            threading.Thread(target=upload, daemon=True).start()
    
    def download_selected(self):
        """Descargar selección"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Selecciona un archivo para descargar")
            return
        
        item = self.tree.item(selection[0])
        name = item['text']
        if not name.startswith('📁'):
            clean_name = name.split(' ', 1)[-1] if ' ' in name else name
            self.download_file(clean_name)
        else:
            messagebox.showinfo("Info", "Para descargar carpetas, selecciona archivos individuales")
    
    def delete_selected(self):
        """Eliminar selección"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        name = item['text']
        clean_name = name.split(' ', 1)[-1] if ' ' in name else name
        
        if not messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente '{clean_name}'?"):
            return
        
        if self.mode == "pc":
            full_path = os.path.join(self.current_path, clean_name)
            try:
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                else:
                    os.remove(full_path)
                self.status_label.config(text=f"🗑️ Eliminado: {clean_name}")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            full_path = self.current_path.rstrip('/') + '/' + clean_name
            self.run_adb_command(f'rm -rf "{full_path}"')
            self.status_label.config(text=f"🗑️ Eliminado: {clean_name}")
            self.refresh()
    
    def copy_selected(self):
        """Copiar"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        name = item['text']
        clean_name = name.split(' ', 1)[-1] if ' ' in name else name
        
        if self.mode == "pc":
            self.clipboard = os.path.join(self.current_path, clean_name)
        else:
            self.clipboard = self.current_path.rstrip('/') + '/' + clean_name
        
        self.clipboard_action = "copy"
        self.status_label.config(text=f"📋 Copiado: {clean_name}")
    
    def cut_selected(self):
        """Cortar"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        name = item['text']
        clean_name = name.split(' ', 1)[-1] if ' ' in name else name
        
        if self.mode == "pc":
            self.clipboard = os.path.join(self.current_path, clean_name)
        else:
            self.clipboard = self.current_path.rstrip('/') + '/' + clean_name
        
        self.clipboard_action = "cut"
        self.status_label.config(text=f"✂️ Cortado: {clean_name}")
    
    def paste_selected(self):
        """Pegar"""
        if not self.clipboard:
            messagebox.showinfo("Info", "No hay nada en el portapapeles")
            return
        
        filename = os.path.basename(self.clipboard)
        
        if self.mode == "pc":
            dest = os.path.join(self.current_path, filename)
            try:
                if os.path.isdir(self.clipboard):
                    shutil.copytree(self.clipboard, dest)
                else:
                    shutil.copy2(self.clipboard, dest)
                
                if self.clipboard_action == "cut":
                    if os.path.isdir(self.clipboard):
                        shutil.rmtree(self.clipboard)
                    else:
                        os.remove(self.clipboard)
                
                self.status_label.config(text=f"📌 Pegado: {filename}")
                self.refresh()
                self.clipboard = None
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            if not self.device_ip:
                messagebox.showerror("Error", "No hay dispositivo Android conectado")
                return
            
            if os.path.exists(self.clipboard):
                self.upload_file()
            else:
                messagebox.showerror("Error", "El archivo original ya no existe")
    
    def go_home(self):
        """Ir a inicio"""
        if self.mode == "pc":
            self.current_path = os.path.expanduser("~")
        else:
            self.current_path = "/sdcard/"
        self.refresh()
    
    def go_up(self):
        """Subir nivel"""
        if self.mode == "pc":
            parent = os.path.dirname(self.current_path)
            if parent and parent != self.current_path:
                self.current_path = parent
                self.refresh()
        else:
            if self.current_path == "/sdcard/":
                return
            path = self.current_path.rstrip('/')
            parts = path.split('/')
            if len(parts) > 2:
                self.current_path = '/'.join(parts[:-1]) + '/'
            else:
                self.current_path = "/sdcard/"
            self.refresh()
    
    def go_to_path(self):
        """Ir a ruta"""
        new_path = self.path_entry.get().strip()
        
        if not self.validate_path(new_path):
            return
        
        if self.mode == "pc":
            if os.path.exists(new_path):
                self.current_path = new_path
                self.refresh()
            else:
                self.status_label.config(text="❌ Ruta no existe")
        else:
            if new_path.startswith('/sdcard/'):
                self.current_path = new_path if new_path.endswith('/') else new_path + '/'
                self.refresh()
            else:
                self.status_label.config(text="❌ Ruta inválida para Android")
    
    def new_folder(self):
        """Nueva carpeta"""
        name = simpledialog.askstring("Nueva carpeta", "Nombre de la carpeta:")
        if not name:
            return
        
        name = name.strip().replace('/', '_').replace('\\', '_')
        
        if self.mode == "pc":
            new_path = os.path.join(self.current_path, name)
            try:
                os.mkdir(new_path)
                self.status_label.config(text=f"📁 Carpeta creada: {name}")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            new_path = self.current_path.rstrip('/') + '/' + name
            self.run_adb_command(f'mkdir "{new_path}"')
            self.status_label.config(text=f"📁 Carpeta creada: {name}")
            self.refresh()
    
    def on_right_click(self, event):
        """Menú contextual"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        name = item['text']
        clean_name = name.split(' ', 1)[-1] if ' ' in name else name
        
        menu = tk.Menu(self.window, tearoff=0, bg=self.colors['panel'], fg=self.colors['cyan'])
        
        menu.add_command(label="📂 Abrir", command=lambda: self.on_double_click(None))
        menu.add_separator()
        
        if self.mode == "android" and not name.startswith('📁'):
            menu.add_command(label="📥 Descargar", command=lambda: self.download_file(clean_name))
        elif self.mode == "pc":
            menu.add_command(label="📂 Abrir con...", command=lambda: self.open_file(clean_name))
        
        menu.add_separator()
        menu.add_command(label="📋 Copiar", command=self.copy_selected)
        menu.add_command(label="✂️ Cortar", command=self.cut_selected)
        menu.add_separator()
        menu.add_command(label="🗑️ Eliminar", command=self.delete_selected)
        menu.add_separator()
        menu.add_command(label="🔄 Renombrar", command=lambda: self.rename_selected(clean_name))
        
        menu.post(event.x_root, event.y_root)
    
    def rename_selected(self, old_name):
        """Renombrar archivo/carpeta"""
        new_name = simpledialog.askstring("Renombrar", "Nuevo nombre:", initialvalue=old_name)
        if not new_name or new_name == old_name:
            return
        
        new_name = new_name.strip().replace('/', '_').replace('\\', '_')
        
        if self.mode == "pc":
            old_path = os.path.join(self.current_path, old_name)
            new_path = os.path.join(self.current_path, new_name)
            try:
                os.rename(old_path, new_path)
                self.status_label.config(text=f"✏️ Renombrado a: {new_name}")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            old_path = self.current_path.rstrip('/') + '/' + old_name
            new_path = self.current_path.rstrip('/') + '/' + new_name
            self.run_adb_command(f'mv "{old_path}" "{new_path}"')
            self.status_label.config(text=f"✏️ Renombrado a: {new_name}")
            self.refresh()
    
    def log(self, message):
        """Log callback"""
        if self.log:
            self.log(message)