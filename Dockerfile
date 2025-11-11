# Dockerfile para Back4App - App_IT-SQSWP03_001_ES_cp
# Aplicación Flask de Quiz sobre estándares ISO

# Usar Python 3.9 slim como imagen base para un contenedor más ligero
FROM python:3.9-slim

# Información del mantenedor
LABEL maintainer="UFV Software Quality <sqs@ufv.es>"
LABEL description="Quiz Application for ISO Standards - Flask Application"
LABEL version="1.0"

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias (incluyendo curl para Back4App)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requisitos primero para aprovechar la cache de Docker
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todos los archivos de la aplicación
COPY . .

# Back4App utiliza variables de entorno dinámicas para el puerto
# Exponer puerto variable que Back4App asignará
EXPOSE $PORT

# Configurar variables de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0

# Comando por defecto para ejecutar la aplicación con puerto dinámico
CMD python -c "import os; print(f'Starting on port: {os.environ.get(\"PORT\", \"5000\")}')" && \
    python -m flask run --host=0.0.0.0 --port=${PORT:-5000}