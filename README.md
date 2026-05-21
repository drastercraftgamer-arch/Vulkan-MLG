# 🌋 VULKAN-MLG v12.0

> Una herramienta para administrar dispositivos Android y PC en una red local.
> 
> *"La inventé solo porque quería tener un programa para controlar las redes y los dispositivos de mi hogar... ¿Por qué no crear un programa para tener control casi total?"*

⚠️ **SOLO para uso en DISPOSITIVOS PROPIOS o con AUTORIZACIÓN EXPLÍCITA.**

---

## 📌 ¿Qué es VULKAN-MLG?

Es una herramienta que permite:
- Escanear dispositivos en tu red local
- Explorar archivos (tanto de PC como de Android)
- Ejecutar comandos ADB
- Controlar un teléfono Android (con su permiso)

> Podía usar cosas como la sincronización con mi PC o FTP para pasar archivos... pero ¿dónde está la diversión?

---

## 🚀 ¿Qué ofrece la aplicación?

### 1. 📡 Pestaña DISPOSITIVOS
- ✅ Escanear red completa
- ✅ Ver IP, MAC, nombre y tipo de cada dispositivo
- ✅ Detectar automáticamente Android (puerto 5555)
- ✅ Seleccionar dispositivo objetivo
- ✅ Guardar dispositivos favoritos

### 2. 🎮 Pestaña CONTROL
- ✅ Ver pantalla del Android (scrcpy)
- ✅ Abrir cámara
- ✅ Grabar video
- ✅ Explorar archivos del dispositivo
- ✅ Bloquear/Desbloquear dispositivo (ARP spoofing)
- ✅ Modo persistente (bloqueo continuo)
- ✅ Enviar notificaciones al Android (no sé si funciona 🤷)
- ✅ Abrir URLs en el navegador
- ✅ Controles: INICIO, ATRÁS, VOLUMEN
- ✅ Ver información del dispositivo
- ✅ Desconectar dispositivo

### 3. 🕵️ Pestaña "ESPIONAJE" (que no es espionaje)
- ✅ Foto stealth (toma foto sin avisar)
- ✅ Grabación de micrófono remota
- ✅ Obtener GPS con enlace a Google Maps
- ✅ Extraer contactos (archivo CSV)
- ✅ Extraer SMS (archivo CSV)
- ✅ Listar aplicaciones instaladas
- ✅ Limpiar evidencia

### 4. ⚔️ Pestaña ATAQUES
- ✅ ARP Spoofing real (bloquea dispositivo de la red)
- ✅ Detener ataque y restaurar red
- ✅ Modo persistente avanzado
- ✅ Restaurar todo

### 5. 💾 Pestaña BACKUPS
- ✅ Seleccionar carpeta de destino
- ⚠️ Backup completo (EN DESARROLLO CTM!!)
- ⚠️ Backup de contactos y SMS (EN DESARROLLO)
- ⚠️ Backup de apps (EN DESARROLLO)
- ⚠️ Backup de fotos/videos (EN DESARROLLO)

### 6. 💻 Pestaña CONSOLA
- ✅ Ejecutar comandos ADB manualmente
- ✅ Ver logs en tiempo real
- ✅ Comandos peligrosos requieren confirmación

---

## 🔧 Cómo configurar todo (paso a paso)

### Paso 1: Instalar Python
1. Ve a [python.org](https://python.org)
2. Descarga Python 3.7 o superior
3. Instálalo y **marca "Add to PATH"**
4. Verifica: `python --version`

### Paso 2: ADB y scrcpy
> **¡Ya vienen incluidos en el proyecto CTM!** Pero si no:

**ADB:**
- Descarga de [developer.android.com](https://developer.android.com/studio/releases/platform-tools)
- Extrae y copia a la carpeta `Adb/`

**Scrcpy:**
- Descarga de [github.com/Genymobile/scrcpy](https://github.com/Genymobile/scrcpy/releases)
- Copia `scrcpy.exe` a `Adb/`

### Paso 3: Configurar el móvil Android
1. Ve a Configuración → Acerca del teléfono
2. Toca "Número de compilación" 7 veces (activa Opciones de Desarrollador)
3. Ve a Opciones de Desarrollador
4. Activa **"Depuración USB"**
5. Activa **"Depuración USB (seguridad)"** si existe
6. Conecta el móvil por USB
7. En el móvil, **ACEPTA la huella RSA**
8. Para usar por WiFi:
   ```bash
   adb tcpip 5555
   adb connect IP_DEL_MÓVIL:5555

### Paso 4: Ejecutar el programa
Opción A (Recomendada):
  1. Haz doble clic en "Configurar.bat" (solo la primera vez)
  2. Haz doble clic en "Iniciar.bat"

Opción B (Manual):
  1. Abre CMD en la carpeta del proyecto
  2. pip install scapy pillow
  3. python main.py

### Paso 5: Primer uso
1. En la pestaña "DISPOSITIVOS", haz clic en "ESCANEAR"
2. Selecciona tu dispositivo Android de la lista
3. Haz clic en "SELECCIONAR"
4. Ve a la pestaña "CONTROL" para probar funciones

## ❌ POSIBLES ERRORES Y SOLUCIONES

ERROR 1: "ADB no encontrado"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Solución: Descarga platform-tools y copia adb.exe a la carpeta Adb/

ERROR 2: "No se pudo conectar al dispositivo"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Solución: 
   - Verifica que USB debugging esté ACTIVADO
   - Acepta la huella RSA en el móvil
   - Móvil y PC en la misma red WiFi
   - Puerto 5555 abierto (adb tcpip 5555)

ERROR 3: "scrcpy no encontrado"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Solución: Descarga scrcpy.exe y copia a la carpeta Adb/

ERROR 4: "ARP spoofing no funciona"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Solución: 
   - Ejecutar como ADMINISTRADOR en Windows
   - En Linux/Mac usar sudo
   - Instalar scapy: pip install scapy

ERROR 5: "La ventana no se ve completa"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Solución: La ventana es redimensionable. Ajusta el tamaño manualmente.

ERROR 6: "Error obteniendo gateway"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Solución: 
   - Verifica que tengas conexión a internet
   - El programa usará IP por defecto (192.168.1.1)

## 📝 DEPENDENCIAS (qué instala Configurar.bat)

- scapy        → Para paquetes ARP (arp spoofing)
- pillow       → Para procesamiento de imágenes (backups)
- tkinter      → Interfaz gráfica (viene con Python)
- subprocess   → Ejecutar comandos del sistema
- threading    → Para operaciones en segundo plano
- socket       → Comunicación de red

## 🛡️ CONSEJOS DE SEGURIDAD

PARA TÍ:
  1. NO uses esto en dispositivos ajenos sin permiso
  2. NO presumas de ser "hacker" - te puedes meter en líos por p3ndejo
  3. SIEMPRE confirma antes de acciones peligrosas (bloquear, eliminar)

PARA TUS DISPOSITIVOS :
  1. Desactiva "Depuración USB" cuando no la uses
  2. No conectes tu móvil a WiFi públicas con debugging activado... ¡¡Por obvias razones ctm!!

## 📜 NOTA LEGAL

ESTE SOFTWARE ES SOLO PARA FINES "EDUCATIVOS".

El autor NO se responsabiliza por:
  - Uso indebido de la herramienta
  - Daños a dispositivos propios o ajenos
  - Problemas legales derivados del mal uso
  - Si se te enfria la pizza

AL USAR ESTA HERRAMIENTA, ACEPTAS:
  ✅ Usarla SOLO en dispositivos de tu propiedad
  ✅ Obtener permiso EXPLÍCITO antes de usar en dispositivos ajenos
  ✅ No utilizarla para actividades ilegales o maliciosas


## ✨ AGRADECIMIENTOS ESPECIALES:


- A mi pc por aguantar mientras hacia el programa
- A mi pan con queso por darme energía
- A mi silla

# VULKAN-MLG v12.0 - FIN DE LA GUÍA 
