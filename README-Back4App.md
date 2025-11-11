# 🚀 Guía de Despliegue en Back4App - ACTUALIZADA

## ⚠️ SOLUCIÓN AL ERROR: "Either dockerfile must expose tcp port or define port in settings"

### El Problema
Back4App requiere que el `Dockerfile` tenga un comando `EXPOSE` explícito para detectar el puerto de la aplicación.

### ✅ Solución Aplicada
He actualizado el `Dockerfile` con la configuración correcta:

```dockerfile
# Exponer puerto 5000 para Back4App
EXPOSE 5000

# Ejecutar la aplicación 
CMD ["python", "app.py"]
```

### Configuración del Puerto en app.py
El archivo `app.py` ya está configurado para manejar el puerto dinámico de Back4App:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

**Cómo funciona:**
- Back4App asigna automáticamente un puerto usando la variable `PORT`
- Si no existe `PORT`, usa el puerto 5000 por defecto
- El `EXPOSE 5000` en el Dockerfile permite que Back4App detecte el puerto correctamente

## 📋 Pasos Actualizados para Desplegar

### 1. Verificar Archivos
✅ **Dockerfile** - Actualizado con `EXPOSE 5000`
✅ **app.py** - Configurado para puerto dinámico  
✅ **requirements.txt** - Dependencias completas
✅ **.dockerignore** - Optimizado para Back4App

### 2. Desplegar en Back4App

1. **Comprimir proyecto** (ZIP) o **subir a Git**
2. **Crear app** en Back4App → "Container as a Service"
3. **Subir código** → Back4App detectará automáticamente el Dockerfile
4. **Deploy** → Esperar 5-10 minutos para el build

### 3. Verificar Despliegue

Una vez completado:
- ✅ **Puerto detectado:** 5000
- ✅ **Estado:** Running
- ✅ **URL disponible:** https://tu-app.back4app.io

## 🔧 Configuración Técnica

### Dockerfile Optimizado para Back4App:
```dockerfile
FROM python:3.9-slim
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

# ⚠️ IMPORTANTE: EXPOSE explícito para Back4App
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# ⚠️ IMPORTANTE: Comando simple para Back4App
CMD ["python", "app.py"]
```

## 🚨 Errores Comunes y Soluciones

### ❌ Error: "Either dockerfile must expose tcp port..."
**Causa:** Falta `EXPOSE` en el Dockerfile
**Solución:** ✅ Ya corregido - `EXPOSE 5000` añadido

### ❌ Error: "Container failed to start"
**Causa:** Puerto mal configurado en app.py
**Solución:** ✅ Ya corregido - Puerto dinámico configurado

### ❌ Error: "Build failed"
**Verificar:**
- Todos los archivos están presentes
- `requirements.txt` es válido
- No hay errores de sintaxis en el código

## 🧪 Test Local Antes de Desplegar

```bash
# Construir imagen Docker
docker build -t iso-quiz-test .

# Probar localmente
docker run -p 5000:5000 iso-quiz-test

# Verificar que funciona en http://localhost:5000
```

## 📱 Funcionalidad de la Aplicación

Una vez desplegada, tu aplicación incluirá:

- **📚 Quiz interactivo** sobre estándares ISO
- **🌍 Multiidioma** (Español/Inglés)  
- **📊 Evaluación automática** con puntuaciones
- **💡 Definiciones detalladas** de conceptos ISO
- **🎯 Preguntas específicas** por estándar (ISO 9241-11, ISO/IEC 25010, etc.)

## 🔗 URLs de Acceso

Después del despliegue:
- **Aplicación principal:** `https://tu-app.back4app.io`
- **Modo español:** `https://tu-app.back4app.io?lang=es`
- **Modo inglés:** `https://tu-app.back4app.io?lang=en`

## 📞 Soporte Técnico

**Para problemas con el despliegue:**
- Revisa los logs en Back4App Dashboard
- Verifica que el puerto 5000 esté detectado
- Confirma que la aplicación inicia correctamente

**Contacto:** sqs@ufv.es

---

### 🎉 ¡LISTO PARA DESPLEGAR!

Con el `Dockerfile` corregido, tu aplicación debería desplegarse exitosamente en Back4App sin errores de puerto.

## 📋 Pasos para Desplegar en Back4App

### 1. Preparar tu cuenta de Back4App

1. **Regístrate/Inicia sesión** en [Back4App](https://www.back4app.com/)
2. **Verifica tu cuenta** si es nueva

### 2. Crear una nueva aplicación

1. En el dashboard de Back4App, haz clic en **"Create a new app"**
2. Selecciona **"Backend as a Service"**
3. Elige **"Container as a Service"** para aplicaciones Docker
4. Asigna un nombre a tu aplicación (ej: "iso-quiz-app")

### 3. Configurar el despliegue

#### **Opción A: Conectar repositorio Git (Recomendado)**

1. **Sube tu código a un repositorio Git:**
   ```bash
   # Inicializar git si no existe
   git init
   git add .
   git commit -m "Ready for Back4App deployment"
   
   # Subir a GitHub/GitLab
   git remote add origin <tu-repositorio-url>
   git push -u origin main
   ```

2. **En Back4App:**
   - Selecciona **"Connect your Git repository"**
   - Conecta tu cuenta de GitHub/GitLab
   - Selecciona el repositorio con tu aplicación
   - Back4App detectará automáticamente el `Dockerfile`

#### **Opción B: Subir archivos directamente**

1. **Comprimir archivos necesarios:**
   - Incluir: `app.py`, `requirements.txt`, `Dockerfile`, `templates/`, `static/`, `definitios_*.md`
   - Excluir: `venv/`, `__pycache__/`, `.git/`

2. **En Back4App:**
   - Selecciona **"Upload your code"**
   - Sube el archivo ZIP
   - Back4App detectará automáticamente el `Dockerfile`

### 4. Configurar variables de entorno

En la sección **"Environment Variables"** de Back4App, añade:

```
FLASK_APP=app.py
FLASK_ENV=production
FLASK_RUN_HOST=0.0.0.0
```

### 5. Configurar el contenedor

- **Puerto:** Back4App asignará automáticamente (no configurar manualmente)
- **Memoria:** 512MB (suficiente para la aplicación)
- **CPU:** 0.5 cores
- **Dockerfile path:** `/Dockerfile` (raíz del proyecto)

### 6. Desplegar

1. Haz clic en **"Deploy"**
2. Back4App construirá la imagen Docker automáticamente
3. El proceso puede tardar 2-5 minutos
4. Una vez completado, recibirás una URL pública

## 🔧 Configuraciones Específicas de Back4App

### Estructura de archivos requerida:
```
tu-proyecto/
├── Dockerfile          ✅ (Configurado para Back4App)
├── app.py             ✅ (Puerto dinámico configurado)
├── requirements.txt   ✅
├── .dockerignore      ✅
├── templates/         ✅
├── static/           ✅
├── definitios_es.md  ✅
├── definitios_en.md  ✅
└── back4app.yml      ✅ (Opcional)
```

### Variables automáticas de Back4App:
- `PORT` - Puerto asignado dinámicamente
- `DATABASE_URL` - Si usas base de datos
- `REDIS_URL` - Si usas Redis

## 🌐 Acceso a tu aplicación

Una vez desplegada, tendrás:

- **URL principal:** `https://tu-app-name.back4app.io`
- **Español:** `https://tu-app-name.back4app.io?lang=es`
- **Inglés:** `https://tu-app-name.back4app.io?lang=en`

## 🔍 Monitoreo y Logs

### Ver logs de la aplicación:
1. En el dashboard de Back4App
2. Ve a tu aplicación
3. Sección **"Logs"**
4. Filtra por **"Application Logs"**

### Métricas de rendimiento:
- **CPU Usage**
- **Memory Usage**
- **Response Times**
- **Error Rates**

## 🛠️ Solución de Problemas

### Error: "Failed to build image"

**Posibles causas:**
1. Archivo `requirements.txt` mal formateado
2. Dependencias incompatibles
3. Dockerfile con errores de sintaxis

**Solución:**
```bash
# Probar localmente primero
docker build -t test-app .
docker run -p 5000:5000 test-app
```

### Error: "Container failed to start"

**Revisar en logs de Back4App:**
- Variables de entorno
- Puerto binding
- Errores de la aplicación Flask

### Error: "Application timeout"

**Back4App tiene límites de tiempo:**
- Aumentar recursos del contenedor
- Optimizar tiempo de inicio de Flask
- Verificar health check endpoint

## 💰 Costos de Back4App

### Plan gratuito incluye:
- **25,000 requests/month**
- **1GB storage**
- **1GB bandwidth**
- **100MB RAM por contenedor**

### Para aplicaciones con más tráfico:
- **Starter:** $5/month
- **Pro:** $25/month
- **Business:** Precios personalizados

## 🔒 Seguridad

### Configuraciones recomendadas:
1. **HTTPS automático** (habilitado por defecto)
2. **Environment variables** para secretos
3. **CORS configurado** apropiadamente
4. **Rate limiting** si es necesario

## 📈 Escalabilidad

### Auto-scaling en Back4App:
- **Horizontal scaling:** Múltiples instancias
- **Vertical scaling:** Más RAM/CPU
- **Load balancing** automático
- **Health checks** integrados

## 🔄 Actualizaciones

### Para actualizar la aplicación:
1. **Push nuevo código** al repositorio Git
2. **Auto-deploy** se activará automáticamente
3. O usar **"Redeploy"** en el dashboard

### Rolling updates:
- Back4App mantiene la aplicación disponible durante actualizaciones
- **Zero downtime deployments**

## 📞 Soporte

### Si tienes problemas:
1. **Documentación oficial:** [docs.back4app.com](https://docs.back4app.com)
2. **Soporte técnico:** support@back4app.com
3. **Comunidad:** Discord y foros oficiales
4. **Stack Overflow:** Tag `back4app`

---

## ✨ ¡Tu aplicación está lista para Back4App!

Con estos archivos configurados, tu aplicación Flask debería desplegarse sin problemas en Back4App. El Dockerfile está optimizado para su plataforma y la aplicación maneja puertos dinámicos correctamente.