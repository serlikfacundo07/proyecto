@echo off
title Sistema de Analitica Retail
echo ==========================================
echo    INICIANDO SISTEMA DE ANALITICA
echo ==========================================
echo.

echo [1/2] Iniciando el motor de IA (con entorno virtual)...

start "Motor IA" cmd /k "venv\Scripts\activate && python index.py"

echo [2/2] Levantando el Panel de Control (con entorno virtual)...
start "Dashboard" cmd /k "venv\Scripts\activate && streamlit run dashboard.py"

echo.
echo ¡Sistema iniciado con exito! 
echo Podes cerrar esta ventanita negra si queres.
timeout /t 5 >nul
exit