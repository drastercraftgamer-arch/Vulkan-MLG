# ui/styles.py - Estilos modernos y oscuros
import tkinter as tk
from tkinter import ttk
import platform

# Kirynota: Ptm, los emojis se ven bien pinche feos una de dos: 
# Python no es muy compatible con emojis o es la fuente (Pendiente por arreglar)

class ModernStyles:
    """Estilos modernos y oscuros para toda la aplicación"""
    
    COLORS = {
        'bg': '#0f0f0f',
        'bg_sec': '#1a1a1a',
        'panel': '#252526',
        'panel_light': '#2d2d30',
        'accent': '#0078d4',
        'accent_hover': '#1a8cff',
        'success': '#6bce5c',
        'warning': '#ffcc00',
        'error': '#ff6b6b',
        'info': '#00ffff',
        'text': '#cccccc',
        'text_bright': '#ffffff',
        'text_dim': '#888888',
        'border': '#3e3e42',
    }
    
    if platform.system() == 'Windows':
        EMOJI_FONT = ('Segoe UI Emoji', 9)
        NORMAL_FONT = ('Segoe UI', 9)
        BOLD_FONT = ('Segoe UI', 9, 'bold')
        CONSOLE_FONT = ('Consolas', 9)
    else:
        EMOJI_FONT = ('Segoe UI', 9)
        NORMAL_FONT = ('Segoe UI', 9)
        BOLD_FONT = ('Segoe UI', 9, 'bold')
        CONSOLE_FONT = ('Monospace', 9)
    
    @classmethod
    def apply_theme(cls, root):
        """Aplicar tema a toda la aplicación"""
        root.configure(bg=cls.COLORS['bg'])
        
        # Configurar ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(".", background=cls.COLORS['bg'])
        
        # Notebook (pestañas)
        style.configure("TNotebook", background=cls.COLORS['bg'], borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background=cls.COLORS['panel'],
                       foreground=cls.COLORS['info'],
                       padding=[15, 8],
                       font=cls.BOLD_FONT)
        style.map("TNotebook.Tab",
                 background=[("selected", cls.COLORS['accent'])],
                 foreground=[("selected", cls.COLORS['text_bright'])])
        
        # Treeview
        style.configure("Treeview",
                       background=cls.COLORS['bg_sec'],
                       foreground=cls.COLORS['text'],
                       fieldbackground=cls.COLORS['bg_sec'],
                       borderwidth=0,
                       font=cls.NORMAL_FONT)
        style.map("Treeview",
                 background=[('selected', cls.COLORS['accent'])],
                 foreground=[('selected', cls.COLORS['text_bright'])])
        
        # Treeview heading
        style.configure("Treeview.Heading",
                       background=cls.COLORS['panel'],
                       foreground=cls.COLORS['info'],
                       font=cls.BOLD_FONT,
                       borderwidth=0)
        
        # Combobox
        style.configure("TCombobox",
                       fieldbackground=cls.COLORS['panel'],
                       background=cls.COLORS['panel'],
                       foreground=cls.COLORS['text'],
                       selectbackground=cls.COLORS['accent'],
                       selectforeground=cls.COLORS['text_bright'])
        
        # Scrollbar
        style.configure("Vertical.TScrollbar",
                       background=cls.COLORS['panel'],
                       troughcolor=cls.COLORS['bg_sec'],
                       arrowcolor=cls.COLORS['info'],
                       borderwidth=0)
        style.configure("Horizontal.TScrollbar",
                       background=cls.COLORS['panel'],
                       troughcolor=cls.COLORS['bg_sec'],
                       arrowcolor=cls.COLORS['info'],
                       borderwidth=0)
        
        # LabelFrame
        style.configure("TLabelframe",
                       background=cls.COLORS['panel'],
                       foreground=cls.COLORS['info'],
                       borderwidth=1,
                       relief="solid")
        style.configure("TLabelframe.Label",
                       background=cls.COLORS['panel'],
                       foreground=cls.COLORS['info'],
                       font=cls.BOLD_FONT)
        
        # Progressbar
        style.configure("TProgressbar",
                       background=cls.COLORS['accent'],
                       troughcolor=cls.COLORS['bg_sec'],
                       borderwidth=0)
    
    @classmethod
    def create_button(cls, parent, text, command, variant="default", width=None):
        """Crear botón con estilo moderno"""
        
        colors = {
            "default": (cls.COLORS['panel'], cls.COLORS['info'], cls.COLORS['accent_hover']),
            "primary": (cls.COLORS['accent'], cls.COLORS['text_bright'], cls.COLORS['accent_hover']),
            "success": (cls.COLORS['success'], cls.COLORS['bg'], '#7fff6b'),
            "danger": (cls.COLORS['error'], cls.COLORS['bg'], '#ff8a8a'),
            "warning": (cls.COLORS['warning'], cls.COLORS['bg'], '#ffff66'),
            "info": (cls.COLORS['accent'], cls.COLORS['text_bright'], '#1a8cff'),
            "dark": (cls.COLORS['bg_sec'], cls.COLORS['text'], cls.COLORS['panel']),
        }
        
        bg, fg, hover = colors.get(variant, colors["default"])
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=bg, fg=fg,
                       font=cls.BOLD_FONT,
                       relief=tk.FLAT,
                       cursor="hand2",
                       padx=10,
                       pady=5,
                       activebackground=hover,
                       activeforeground=cls.COLORS['text_bright'])
        
        def on_enter(e):
            btn.config(bg=hover, fg=cls.COLORS['text_bright'])
        
        def on_leave(e):
            btn.config(bg=bg, fg=fg)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        if width:
            btn.config(width=width)
        
        return btn
    
    @classmethod
    def create_entry(cls, parent, **kwargs):
        entry = tk.Entry(parent,
                        bg=cls.COLORS['bg_sec'],
                        fg=cls.COLORS['info'],
                        insertbackground=cls.COLORS['info'],
                        relief=tk.FLAT,
                        font=cls.NORMAL_FONT,
                        **kwargs)
        return entry
    
    @classmethod
    def create_label(cls, parent, text, variant="normal", font=None, **kwargs):
        """Crear label con estilo - CORREGIDO: sin duplicación de font"""
        colors = {
            "normal": cls.COLORS['text'],
            "bright": cls.COLORS['text_bright'],
            "dim": cls.COLORS['text_dim'],
            "info": cls.COLORS['info'],
            "success": cls.COLORS['success'],
            "warning": cls.COLORS['warning'],
            "error": cls.COLORS['error'],
        }
        
        fg = colors.get(variant, cls.COLORS['text'])
        
        if font is None:
            font = cls.NORMAL_FONT
        
        label = tk.Label(parent, text=text, bg=cls.COLORS['bg'], fg=fg, font=font, **kwargs)
        return label
    
    @classmethod
    def create_frame(cls, parent, variant="bg", **kwargs):
        colors = {
            "bg": cls.COLORS['bg'],
            "sec": cls.COLORS['bg_sec'],
            "panel": cls.COLORS['panel'],
        }
        
        bg = colors.get(variant, cls.COLORS['bg'])
        frame = tk.Frame(parent, bg=bg, **kwargs)
        return frame
    
    @classmethod
    def create_label_frame(cls, parent, text, **kwargs):
        frame = tk.LabelFrame(parent, text=text,
                              bg=cls.COLORS['panel'],
                              fg=cls.COLORS['info'],
                              font=cls.BOLD_FONT,
                              **kwargs)
        return frame