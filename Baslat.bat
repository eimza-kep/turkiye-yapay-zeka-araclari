@echo off
chcp 65001 >nul
title Türkiye Yapay Zeka Araçları - Kolay Başlatıcı
cd /d "%~dp0"

echo ======================================================================
echo    🇹🇷 Türkiye Yapay Zeka Araçları - Kolay Başlatıcı
echo ======================================================================
echo.

:: 1. Sistem PATH'inde python kontrolü
where python >nul 2>nul
if %errorlevel% equ 0 (
    python baslat.py
    goto :end
)

:: 2. Python py başlatıcı kontrolü
where py >nul 2>nul
if %errorlevel% equ 0 (
    py baslat.py
    goto :end
)

:: 3. Yerel AppData Python yolları kontrolü
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" baslat.py
    goto :end
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" baslat.py
    goto :end
)
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" baslat.py
    goto :end
)

:: 4. Python bulunamazsa doğrudan Web Portalını tarayıcıda aç
echo [BILGI] Python komut satırında bulunamadı.
echo Web Portalı doğrudan varsayılan internet tarayıcınızda açılıyor...
timeout /t 2 >nul
start "" "%~dp0web\index.html"

:end
