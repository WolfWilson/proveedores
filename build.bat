@echo off
setlocal

set APP_NAME=main
set DIST_DIR=dist
set BUILD_DIR=build

echo [1/3] Limpiando version anterior...
if exist "%DIST_DIR%\%APP_NAME%" (
    rmdir /s /q "%DIST_DIR%\%APP_NAME%"
    echo      Eliminado: %DIST_DIR%\%APP_NAME%
)
if exist "%BUILD_DIR%\%APP_NAME%" (
    rmdir /s /q "%BUILD_DIR%\%APP_NAME%"
    echo      Eliminado: %BUILD_DIR%\%APP_NAME%
)

echo [2/3] Compilando con PyInstaller...
pyinstaller --onedir --noconsole ^
  --optimize 2 ^
  --icon "Source/icon.ico" ^
  --add-data "Source;Source" ^
  --add-data "anto_modulos;anto_modulos" ^
  --name "%APP_NAME%" ^
  main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Fallo la compilacion.
    pause
    exit /b 1
)

echo [3/3] Listo. Ejecutable en: %DIST_DIR%\%APP_NAME%\%APP_NAME%.exe
echo.
pause
