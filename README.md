# ISO Quiz - Aplicación de Retos de Calidad de Software

Una aplicación web simple para poner a prueba los conocimientos sobre estándares de calidad de software a través de preguntas tipo test.

## Características

- Interfaz de usuario sencilla y atractiva
- Soporte para múltiples estándares: ISO/IEC 25010:2023, ISO/IEC/IEEE 29148, ISO 9241
- Preguntas generadas dinámicamente mediante un modelo de lenguaje (Ollama)
- Retroalimentación detallada para cada respuesta
- Sistema de puntuación y resultados finales

## Requisitos

- Python 3.7 o superior
- Flask
- Requests
- Ollama (modelo gpt-oss o similar instalado localmente)

## Instalación

1. Clona este repositorio o descarga los archivos

2. Instala las dependencias:
```
pip install flask requests
```

3. Asegúrate de tener Ollama instalado y el modelo gpt-oss disponible:
```
ollama pull gpt-oss
```

## Uso

1. Inicia el servidor Flask:
```
python app.py
```

2. Abre un navegador web y visita:
```
http://localhost:5000
```

3. Ingresa tu nombre, selecciona un estándar y comienza el reto.

## Estructura del Proyecto

- `app.py`: Aplicación principal Flask
- `templates/index.html`: Plantilla HTML principal
- `static/css/style.css`: Estilos CSS
- `static/js/main.js`: Lógica de interfaz JavaScript

## Personalización

Para añadir más preguntas predefinidas, modifica la función `get_fallback_question()` en `app.py`.

## Limitaciones

- La aplicación depende de Ollama ejecutándose localmente
- Las preguntas predefinidas son limitadas
- No hay persistencia de datos entre sesiones

## Notas

Esta aplicación es para fines educativos. Se recomienda usar un entorno controlado para su ejecución.
