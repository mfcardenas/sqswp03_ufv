# Docker Deployment - ISO Quiz Application

Este directorio contiene los archivos necesarios para ejecutar la aplicación Quiz de Estándares ISO usando Docker.

## Archivos Docker

- `Dockerfile` - Configuración de la imagen Docker
- `docker-compose.yml` - Configuración de Docker Compose
- `.dockerignore` - Archivos excluidos del build
- `docker-run.bat` - Script de utilidades para Windows

## Requisitos Previos

1. **Docker Desktop instalado y ejecutándose**
   - Descargar desde: https://www.docker.com/products/docker-desktop/
   - Asegurarse de que esté iniciado

2. **Puerto 5000 disponible**
   - La aplicación se ejecutará en `http://localhost:5000`

## Métodos de Ejecución

### Opción 1: Script Automatizado (Recomendado)

```bash
# En Windows
docker-run.bat

# Seguir el menú interactivo
```

### Opción 2: Docker Compose

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build

# Parar
docker-compose down
```

### Opción 3: Comandos Docker Manuales

```bash
# 1. Construir la imagen
docker build -t iso-quiz-app .

# 2. Ejecutar el contenedor
docker run -d --name iso-quiz-app -p 5000:5000 iso-quiz-app

# 3. Verificar que esté ejecutándose
docker ps

# 4. Ver logs
docker logs iso-quiz-app

# 5. Parar y eliminar
docker stop iso-quiz-app
docker rm iso-quiz-app
```

## Acceso a la Aplicación

Una vez ejecutándose, accede a:
- **URL Principal:** http://localhost:5000
- **Español:** http://localhost:5000?lang=es
- **Inglés:** http://localhost:5000?lang=en

## Verificación de Funcionamiento

### Verificar que el contenedor esté ejecutándose:
```bash
docker ps
```

### Ver logs de la aplicación:
```bash
docker logs iso-quiz-app
```

### Verificar la salud del contenedor:
```bash
docker inspect --format='{{.State.Health.Status}}' iso-quiz-app
```

## Solución de Problemas

### Error: "Puerto 5000 ya está en uso"

```bash
# Ver qué proceso usa el puerto 5000
netstat -ano | findstr :5000

# Parar contenedor existente
docker stop iso-quiz-app
docker rm iso-quiz-app

# O cambiar el puerto en docker-compose.yml:
ports:
  - "5001:5000"  # Usar puerto 5001 en lugar de 5000
```

### Error: "Docker no está ejecutándose"

1. Iniciar Docker Desktop
2. Esperar a que aparezca el icono en la bandeja del sistema
3. Verificar con: `docker version`

### Error de construcción: "No such file or directory"

1. Verificar que estás en el directorio correcto
2. Verificar que existe el archivo `requirements.txt`
3. Ejecutar desde el directorio que contiene el `Dockerfile`

### Problemas de permisos en Windows

1. Ejecutar Command Prompt como Administrador
2. O configurar Docker Desktop para ejecutar sin privilegios administrativos

## Desarrollo y Depuración

### Ejecutar en modo interactivo:
```bash
docker run -it --rm -p 5000:5000 iso-quiz-app bash
```

### Montar volúmenes para desarrollo:
```bash
docker run -d --name iso-quiz-app \
  -p 5000:5000 \
  -v ${PWD}/static:/app/static \
  -v ${PWD}/templates:/app/templates \
  iso-quiz-app
```

### Reconstruir sin cache:
```bash
docker build --no-cache -t iso-quiz-app .
```

## Configuración Avanzada

### Variables de Entorno

Puedes configurar variables de entorno en el archivo `docker-compose.yml`:

```yaml
environment:
  - FLASK_ENV=development  # Para modo desarrollo
  - FLASK_DEBUG=1          # Para depuración
```

### Persistencia de Datos

Si necesitas persistir datos, puedes añadir volúmenes:

```yaml
volumes:
  - quiz_data:/app/data
```

## Limpieza

### Limpiar completamente:
```bash
# Parar y eliminar contenedor
docker stop iso-quiz-app
docker rm iso-quiz-app

# Eliminar imagen
docker rmi iso-quiz-app

# Limpiar imágenes no utilizadas
docker system prune
```

## Recursos Adicionales

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Flask Deployment with Docker](https://flask.palletsprojects.com/en/2.0.x/deploying/)