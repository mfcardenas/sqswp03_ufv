@echo off
REM docker-run.bat
REM Script para construir y ejecutar la aplicación Flask con Docker

echo ====================================================
echo     Quiz ISO Standards - Docker Deployment
echo ====================================================
echo.

REM Verificar si Docker está ejecutándose
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker no está ejecutándose o no está instalado.
    echo Por favor, inicia Docker Desktop y vuelve a intentar.
    pause
    exit /b 1
)

echo Docker está ejecutándose correctamente.
echo.

REM Menú de opciones
:menu
echo Selecciona una opción:
echo 1. Construir la imagen Docker
echo 2. Ejecutar el contenedor
echo 3. Construir y ejecutar (recomendado)
echo 4. Parar el contenedor
echo 5. Ver logs del contenedor
echo 6. Eliminar contenedor e imagen
echo 7. Salir
echo.
set /p choice="Ingresa tu opción (1-7): "

if "%choice%"=="1" goto build
if "%choice%"=="2" goto run
if "%choice%"=="3" goto build_and_run
if "%choice%"=="4" goto stop
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto cleanup
if "%choice%"=="7" goto exit
echo Opción inválida, intenta de nuevo.
goto menu

:build
echo.
echo Construyendo la imagen Docker...
docker build -t iso-quiz-app .
if %errorlevel% neq 0 (
    echo ERROR: Falló la construcción de la imagen.
    pause
    goto menu
)
echo Imagen construida exitosamente.
echo.
goto menu

:run
echo.
echo Ejecutando el contenedor...
docker run -d --name iso-quiz-app -p 5000:5000 iso-quiz-app
if %errorlevel% neq 0 (
    echo ERROR: Falló la ejecución del contenedor.
    pause
    goto menu
)
echo Contenedor ejecutándose en http://localhost:5000
echo.
goto menu

:build_and_run
echo.
echo Parando contenedor existente (si existe)...
docker stop iso-quiz-app 2>nul
docker rm iso-quiz-app 2>nul
echo.
echo Construyendo la imagen Docker...
docker build -t iso-quiz-app .
if %errorlevel% neq 0 (
    echo ERROR: Falló la construcción de la imagen.
    pause
    goto menu
)
echo.
echo Ejecutando el contenedor...
docker run -d --name iso-quiz-app -p 5000:5000 iso-quiz-app
if %errorlevel% neq 0 (
    echo ERROR: Falló la ejecución del contenedor.
    pause
    goto menu
)
echo.
echo ====================================================
echo   Aplicación ejecutándose exitosamente!
echo   URL: http://localhost:5000
echo ====================================================
echo.
goto menu

:stop
echo.
echo Parando el contenedor...
docker stop iso-quiz-app
docker rm iso-quiz-app
echo Contenedor parado y eliminado.
echo.
goto menu

:logs
echo.
echo Mostrando logs del contenedor (Ctrl+C para salir):
docker logs -f iso-quiz-app
echo.
goto menu

:cleanup
echo.
echo Eliminando contenedor e imagen...
docker stop iso-quiz-app 2>nul
docker rm iso-quiz-app 2>nul
docker rmi iso-quiz-app 2>nul
echo Limpieza completada.
echo.
goto menu

:exit
echo.
echo Saliendo...
exit /b 0