@echo off
title Configurar Vulkan-MLG
color 0A
cd /d "%~dp0"

echo ========================================
echo    CONFIGURANDO VULKAN-MLG
echo ========================================
echo.

:: Instalar dependencias
echo [1/2] Instalando las dependencias...
pip install scapy pillow

:: Crear carpetas
echo [2/2] Creando carpetas...
mkdir backups 2>nul
mkdir Adb 2>nul

:: Metiendo virus (Nah es bromas)
echo [1/2] Metiendo virus bien malotes para hackearla la PC JAJAJAJAJ

echo.
echo ========================================
echo    CONFIGURACION COMPLETADA
echo ========================================
echo.
echo Para usar ADB, descarga platform-tools
echo y copia adb.exe en la carpeta Adb/
echo.
pause