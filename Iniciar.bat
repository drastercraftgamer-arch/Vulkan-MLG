@echo off
title Vulkan-MLG
color 0A
cd /d "%~dp0"

echo ========================================
echo    VULKAN-MLG v12.0
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no instalado
    pause
    exit /b 1
)

:: Verificar ADB
if exist "Adb\adb.exe" (
    set "PATH=%CD%\Adb;%PATH%"
    echo [OK] ADB encontrado
)

:: Iniciar
echo [OK] Iniciando...
python main.py

pause