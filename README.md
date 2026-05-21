
##                       "VULKAN-MLG v12.0 - GUÍA COMPLETA"


## **📌 ¿QUÉ ES VULKAN-MLG?**

Es una herramienta para administrar dispositivos Android y PC en una 
red local. Permite escanear dispositivos, explorar archivos, ejecutar comandos 
ADB y controlar un teléfono Android. La inventé solo porque quería tener un 
programa para controlar las redes y los dispositivos de mi hogar...
Si, podía usar cosas como la sincronización ocn mi PC o el ftp si quería pasar
archivos. Pero... ¿Por que no crear un programa para tener control casi total?

⚠️ SOLO para uso en DISPOSITIVOS PROPIOS o con AUTORIZACIÓN EXPLÍCITA.

## 📋 FUNCIÓN DE CADA ARCHIVO 

--------------------- ARCHIVOS PRINCIPALES ---------------------

📄 main.py
   → Inicia la aplicación. Crea la ventana principal y carga la interfaz.
   → Configura el tamaño, título y eventos de cierre.

📄 Iniciar.bat
   → Script para Windows. Verifica Python, busca ADB y ejecuta main.py.

📄 Configurar.bat
   → Instala dependencias (scapy, pillow) y crea carpetas necesarias.

📄 config.json
   → Guarda configuración: dispositivos favoritos, ajustes de red, backups.

--------------------- CARPETA core/ ---------------------

📄 vulkan_core.py
   → El CEREBRO del programa. Coordina todas las funciones:
     - Escanear red
     - Conectar a dispositivos Android
     - Ejecutar comandos ADB
     - Control de ataques
     - Llamar a herramientas de espionaje

📄 network_scanner.py
   → Escáner de red. Detecta dispositivos conectados al WiFi.
   → Usa ping para encontrar IPs activas y detecta si son Android por puerto 5555.

📄 adb_controller.py
   → Controlador ADB. Maneja la comunicación con Android:
     - Conectar/desconectar dispositivos
     - Enviar comandos shell
     - Abrir cámara, URLs, notificaciones
     - Iniciar scrcpy

📄 arp_spoofer.py
   → ARP Spoofing. Intercepta el tráfico de red de un dispositivo.
   → Requiere permisos de administrador. SOLO para pruebas en red propia.

📄 security_manager.py
   → Gestor de seguridad (opcional). Registra operaciones "peligrosas".

--------------------- CARPETA ui/ ---------------------

📄 modern_ui.py
   → INTERFAZ VISUAL. Crea todas las pestañas:
     - DISPOSITIVOS: lista de equipos en la red
     - CONTROL: botones para manejar el Android
     - ESPIONAJE: herramientas de espionaje (foto, GPS, etc.)
     - ATAQUES: ARP spoofing y bloqueos
     - BACKUPS: respaldo de datos
     - CONSOLA: comandos ADB manuales

📄 styles.py
   → ESTILOS Y TEMAS. Define colores, fuentes y efectos visuales.

--------------------- CARPETA tools/ ---------------------

📄 file_explorer.py
   → EXPLORADOR DE ARCHIVOS DUAL.
     - Modo PC: navega por tu computadora
     - Modo Android: navega por el teléfono (requiere ADB)
     - Funciones: copiar, pegar, eliminar, crear carpetas, subir/bajar archivos

📄 spy_tools.py
   → HERRAMIENTAS DE "ESPIONAJE" (requieren Android conectado):
     - FOTO STEALTH: toma foto sin que el usuario sepa
     - GRABAR MICRÓFONO: graba audio por X segundos
     - OBTENER GPS: coordenadas y enlace a Google Maps
     - EXTRAER CONTACTOS: guarda contactos en CSV
     - EXTRAER SMS: guarda mensajes en CSV
     - APPS INSTALADAS: lista todas las apps
     - LIMPIAR EVIDENCIA: borra archivos temporales creados

--------------------- CARPETA utils/ ---------------------

📄 logger.py
   → SISTEMA DE LOGS. Muestra mensajes con timestamp en la consola.
   → Colores: CYAN (info), GREEN (éxito), RED (error), YELLOW (advertencia)

📄 config.py
   → GESTOR DE CONFIGURACIÓN. Guarda y carga ajustes desde config.json.



## 🚀 QUÉ OFRECE LA APLICACIÓN??? (FUNCIONES "SEMICOMPLETAS." 


1. 📡 PESTAÑA DISPOSITIVOS
   ✅ Escanear red completamente
   ✅ Ver IP, MAC, nombre y tipo de cada dispositivo
   ✅ Detectar automáticamente Android (puerto 5555)
   ✅ Seleccionar dispositivo objetivo
   ✅ Guardar dispositivos favoritos

2. 🎮 PESTAÑA CONTROL
   ✅ Ver pantalla del Android (scrcpy)
   ✅ Abrir cámara
   ✅ Grabar video
   ✅ Explorar archivos del dispositivo
   ✅ Bloquear/Desbloquear dispositivo (ARP spoofing)
   ✅ Modo persistente (bloqueo continuo)
   ✅ Enviar notificaciones al Android (Esta wea no creo que funcione...)
   ✅ Abrir URLs en el navegador del Android
   ✅ Controles básicos: INICIO, ATRÁS, VOLUMEN
   ✅ Ver información del dispositivo (modelo, Android, batería)
   ✅ Desconectar dispositivo

3. 🕵️ PESTAÑA DE ESPIONAJE QUE NO ES ESPIONAJE
   ✅ Foto stealth (toma foto sin avisar)
   ✅ Grabación de micrófono remota
   ✅ Obtener GPS con enlace a Google Maps
   ✅ Extraer todos los contactos (archivo CSV)
   ✅ Extraer todos los SMS (archivo CSV)
   ✅ Listar aplicaciones instaladas
   ✅ Limpiar evidencia (borra archivos creados)

4. ⚔️ PESTAÑA ATAQUES
   ✅ ARP Spoofing real (bloquea dispositivo de la red)
   ✅ Detener ataque y restaurar red
   ✅ Modo persistente avanzado
   ✅ Restaurar todo (detiene todos los ataques)

5. 💾 PESTAÑA BACKUPS
   ✅ Seleccionar carpeta de destino
   ✅ Backup completo (EN DESARROLLO CTM!!)
   ✅ Backup de contactos y SMS (EN DESARROLLO CTM!!)
   ✅ Backup de apps (EN DESARROLLO CTM!!)
   ✅ Backup de fotos/videos (EN DESARROLLO CTM!!)

6. 💻 PESTAÑA CONSOLA
   ✅ Ejecutar comandos ADB manualmente
   ✅ Ver logs en tiempo real
   ✅ Comandos peligrosos requieren confirmación



## 🔧 CÓMO CONFIGURAR TODO (PASO A PASO)


PASO 1: INSTALAR PYTHON
------------------------
Si no tienes Python:
  1. Ve a python.org
  2. Descarga Python 3.7 o superior
  3. Instálalo. MARCA "Add to PATH"
  4. Verifica: Abre CMD y escribe "python --version"

PASO 2: DESCARGAR ADB Y SCRCPY (Si de alguna manera no lo tienes... ¡YA VIENE CON EL PROYECTO CTM!)
------------------------------
ADB (Android Debug Bridge):
  1. Ve a developer.android.com/studio/releases/platform-tools
  2. Descarga el ZIP para Windows
  3. Extrae los archivos
  4. Copia TODOS los archivos a la carpeta "Adb/" de este proyecto

Scrcpy (ver pantalla del móvil):
  1. Ve a github.com/Genymobile/scrcpy/releases
  2. Descarga scrcpy-win64-v2.x.zip
  3. Extrae scrcpy.exe y scrcpy-noconsole.exe
  4. Copia a la carpeta "Adb/"

Estructura final de "Adb/":
  Adb/
  ├── adb.exe
  ├── AdbWinApi.dll
  ├── AdbWinUsbApi.dll
  ├── scrcpy.exe
  ├── scrcpy-noconsole.exe
  └── ... (otros archivos)

PASO 3: CONFIGURAR EL MÓVIL ANDROID
-----------------------------------
Para que funcione el control remoto:
  1. Ve a Configuración → Acerca del teléfono
  2. Toca "Número de compilación" 7 veces (activa Opciones de Desarrollador)
  3. Ve a Configuración → Opciones de Desarrollador
  4. Activa "Depuración USB"
  5. Activa "Depuración USB (seguridad)") si existe
  6. Conecta el móvil por USB a la PC
  7. En el móvil, ACEPTA la huella RSA (ventana emergente)
  8. Para usar por WiFi: 
     - Conecta móvil por USB
     - Ejecuta: adb tcpip 5555
     - Desconecta USB
     - Conecta por WiFi: adb connect IP_DEL_MÓVIL:5555

PASO 4: EJECUTAR EL PROGRAMA
----------------------------
Opción A (Recomendada):
  1. Haz doble clic en "Configurar.bat" (solo la primera vez)
  2. Haz doble clic en "Iniciar.bat"

Opción B (Manual):
  1. Abre CMD en la carpeta del proyecto
  2. pip install scapy pillow
  3. python main.py

PASO 5: PRIMER USO
------------------
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



## ⚙️ REQUISITOS DEL SISTEMA: CORRE EN CUALQUIER COSA QUE TENGA PANTALLA IGUAL QUE DOOM!!! (na mentira...)


"MÍNIMO":
  - Windows 7/8/10/11, Linux o Mac
  - Python 3.7 o superior
  - 2GB RAM
  - Conexión WiFi o Ethernet (P3ndejo si tienes esto es porque tienes internet)

RECOMENDADO:
  - Windows 10/11
  - Python 3.10+
  - 4GB RAM
  - Tarjeta WiFi compatible con modo monitor (para ARP spoofing)

PARA ANDROID:
  - Android 5.0 o superior 
  - Depuración USB activada


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

## 📞 "AYUDA" Y "SOPORTE" 

Si tienes problemas:
  1. Revisa este archivo, la solución puede estar aquí. (P.D: No va a estar...)
  2. Verifica que ADB funciona: Abre CMD → adb devices
  3. Verifica que Python está instalado: python --version
  4. Ejecuta Configurar.bat de nuevo

ERRORES COMUNES DE ADB:
  - "device offline" → Rechaza la huella RSA en el móvil
  - "unauthorized" → No has aceptado la depuración USB
  - "cannot connect" → Puerto 5555 cerrado o WiFi diferente

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

## ✨ AGRADECIMIENTOS:

- A mi pc por aguantar mientras hacia el programa
- A mi pan con queso por darme energía
- A mi silla

#                   VULKAN-MLG v12.0 - FIN DE LA GUÍA 

