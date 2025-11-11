# Manual de Usuario: ISO Quiz App

## 1. Introducción

Bienvenido a **ISO Quiz App**, una aplicación web interactiva diseñada para evaluar y mejorar tus conocimientos sobre importantes estándares de calidad de software. A través de un cuestionario dinámico, podrás poner a prueba tu comprensión de normativas como ISO/IEC 25010, ISO/IEC/IEEE 29148 e ISO 9241.

La aplicación utiliza un modelo de lenguaje de inteligencia artificial (Ollama) para generar preguntas únicas en tiempo real, ofreciendo una experiencia de aprendizaje siempre nueva. Además, cuenta con soporte multilingüe (español e inglés) y una interfaz clara y sencilla.

## 2. Características Principales

- **Soporte Multilingüe:** Interfaz y contenido disponible en **Español** e **Inglés**.
- **Generación Dinámica de Preguntas:** Utiliza un modelo de IA (Ollama) para crear preguntas al momento, asegurando que cada cuestionario sea diferente.
- **Preguntas de Respaldo:** Si el modelo de IA no está disponible, la aplicación proporciona preguntas predefinidas para no interrumpir la experiencia.
- **Indicador de Origen:** Muestra claramente si una pregunta fue generada por la IA (🤖) o si es una pregunta de respaldo (📚).
- **Feedback Instantáneo:** Recibe una respuesta visual inmediata (verde para correcto, rojo para incorrecto) después de contestar cada pregunta.
- **Indicador de Carga:** Un aviso visual ("Generando pregunta..." / "Generating question...") informa al usuario cuando la aplicación está trabajando.
- **Interfaz Sencilla:** Un diseño limpio y fácil de usar que te permite concentrarte en el contenido.
- **Resultados Detallados:** Al finalizar, obtendrás un resumen con tu puntuación total.

## 3. Instalación y Puesta en Marcha

Para ejecutar la aplicación en tu máquina local, sigue estos pasos.

### 3.1. Requisitos Previos

Asegúrate de tener instalado lo siguiente:

- **Python 3.7 o superior**.
- **Ollama** con un modelo de lenguaje descargado (ej. `gemma:2b`). Puedes descargarlo desde [ollama.com](https://ollama.com/).
- Un navegador web moderno (Chrome, Firefox, Edge).

### 3.2. Pasos de Instalación

1.  **Descarga el Proyecto:** Clona o descarga el repositorio en una carpeta de tu elección.
2.  **Instala las Dependencias de Python:** Abre una terminal o línea de comandos en la carpeta del proyecto y ejecuta:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Asegúrate de que Ollama esté en ejecución:** Inicia la aplicación de Ollama en tu sistema. Para verificar que funciona y tienes un modelo, abre otra terminal y ejecuta:
    ```bash
    ollama list
    ```
    Deberías ver el modelo que usarás (ej. `gemma:2b`) en la lista.

### 3.3. Iniciar la Aplicación

La forma más sencilla de iniciar la aplicación es usando el script `run.bat`. Simplemente haz doble clic en él.

Este script realizará automáticamente los siguientes pasos:
1.  Creará un entorno virtual de Python.
2.  Instalará las dependencias necesarias.
3.  Iniciará el servidor web de la aplicación.

Una vez que el servidor esté en marcha, verás un mensaje en la terminal indicando que la aplicación está disponible en `http://127.0.0.1:5000`.

## 4. Guía de Uso

### 4.1. Pantalla de Inicio

Al abrir `http://127.0.0.1:5000` en tu navegador, verás la pantalla de inicio.

 <!-- Imagen de ejemplo, no generada -->

1.  **Selector de Idioma:** En la esquina superior derecha, puedes cambiar entre **ES** (Español) y **EN** (Inglés). La interfaz se traducirá automáticamente.
2.  **Nombre:** Introduce tu nombre.
3.  **Estándar:** Selecciona el estándar de calidad sobre el que quieres ser evaluado.
4.  **Número de Preguntas:** Elige cuántas preguntas deseas en tu cuestionario.
5.  **Empezar:** Haz clic en "Empezar" / "Start" para comenzar.

### 4.2. Pantalla de Preguntas

Una vez iniciado el cuestionario, verás la interfaz de preguntas.

1.  **Indicador de Carga:** Antes de que aparezca cada pregunta, verás el mensaje **"Generando pregunta..."**. Esto significa que la aplicación está contactando al modelo de IA.
2.  **Contador de Preguntas:** Muestra tu progreso (ej. "Pregunta 1 de 10").
3.  **Texto de la Pregunta:** El enunciado de la pregunta a responder.
4.  **Indicador de Origen:** Justo debajo de la pregunta, un icono te informa si fue generada por **IA (🤖)** o es una **pregunta de respaldo (📚)**.
5.  **Opciones de Respuesta:** Haz clic en la opción que consideres correcta.
    -   Tu selección se marcará en azul.
    -   Una vez seleccionada, la opción correcta se iluminará en **verde** y las incorrectas en **rojo**.
6.  **Botón "Siguiente Pregunta":** Después de responder, haz clic en este botón para avanzar.

### 4.3. Pantalla de Resultados

Al completar todas las preguntas, la aplicación te mostrará la pantalla de resultados.

- **Puntuación Final:** Verás el número de respuestas correctas sobre el total de preguntas.
- **Botón "Reiniciar":** Te permite volver a la pantalla de inicio para comenzar un nuevo cuestionario.

## 5. Estructura del Proyecto (Visión Técnica)

-   `app.py`: El corazón de la aplicación. Es el servidor web Flask que gestiona la lógica, se comunica con Ollama y sirve las páginas.
-   `mock_ollama.py`: Un script para simular las respuestas del modelo de IA, útil para desarrollo y pruebas sin depender de Ollama.
-   `run.bat`: Script de Windows para facilitar la instalación e inicio de la aplicación.
-   `templates/index.html`: La única plantilla HTML, que contiene la estructura de todas las pantallas de la aplicación.
-   `static/css/style.css`: Define la apariencia visual, los colores, las fuentes y el diseño responsivo.
-   `static/js/main.js`: Controla toda la interactividad del lado del cliente: cambiar de idioma, cargar preguntas, validar respuestas, mostrar resultados y manejar los indicadores de carga.
-   `static/js/translations.js`: Contiene todas las cadenas de texto en español e inglés, permitiendo la funcionalidad multilingüe.
-   `definitions.md`: Este manual de usuario.

## 6. Resolución de Problemas Comunes

-   **El indicador "Generando pregunta..." no desaparece:**
    -   **Causa:** El modelo de IA (Ollama) no está respondiendo o tarda demasiado.
    -   **Solución:** Asegúrate de que la aplicación de Ollama esté en ejecución en tu sistema. Verifica que el modelo de lenguaje esté correctamente descargado y disponible.

-   **La aplicación muestra un error o no se inicia:**
    -   **Causa:** Las dependencias de Python no están instaladas.
    -   **Solución:** Ejecuta `pip install -r requirements.txt` en la terminal desde la carpeta del proyecto.

-   **Los textos aparecen en español aunque seleccioné inglés (o viceversa):**
    -   **Causa:** Puede ser un problema de caché del navegador.
    -   **Solución:** Realiza una recarga forzada de la página (Ctrl + F5 en la mayoría de los navegadores) o limpia la caché de tu navegador.