@echo off
title DGA Detection & Intelligence Platform (Machine Learning)
echo =====================================================================
echo  SISTEM DETEKSI DOMAIN GENERATION ALGORITHM (DGA) BERBASIS MACHINE LEARNING
echo  Security Operations Center (SOC) & Administrator Platform
echo =====================================================================
echo.

cd /d "%~dp0"

if exist "D:\phyton\python.exe" (
    echo Menggunakan Python: D:\phyton\python.exe
    "D:\phyton\python.exe" app.py
) else (
    echo Menjalankan dengan python default sistem...
    python app.py
)

pause
