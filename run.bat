@echo off
rem Archivo de ejecución para Windows
echo ISO Quiz - Iniciando aplicación...

rem Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado o no está en el PATH.
    echo Por favor, instala Python 3.7 o superior.
    pause
    exit /b 1
)

rem Verificar si el entorno virtual existe, si no, crearlo
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

rem Activar entorno virtual
call venv\Scripts\activate.bat

rem Instalar dependencias
echo Instalando dependencias...
pip uninstall -y flask werkzeug
pip install -r requirements.txt

rem Iniciar la aplicación
echo Iniciando la aplicación...
python app.py

pause
