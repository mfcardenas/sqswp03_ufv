from flask import Flask, jsonify, request
import json
import random
import time

# Aplicación de simulación para pruebas sin Ollama
app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate():
    """Simula la API de Ollama para pruebas"""
    data = request.json
    prompt = data.get('prompt', '')
    
    # Simular tiempo de procesamiento
    time.sleep(1)
    
    # Crear una respuesta ficticia basada en el prompt
    if 'ISO/IEC 25010' in prompt:
        response_text = """
        PREGUNTA: ¿Cuál de las siguientes características de ISO/IEC 25010 se refiere a la protección de información?
        OPCIONES:
        A. Usabilidad
        B. Seguridad
        C. Mantenibilidad
        D. Compatibilidad
        RESPUESTA CORRECTA: B
        EXPLICACIÓN: La Seguridad es la característica que protege la información y los datos para que solo las personas autorizadas puedan acceder a ellos. Esta característica incluye subcaracterísticas como confidencialidad, integridad, no repudio, responsabilidad y autenticidad.
        """
    elif 'ISO/IEC/IEEE 29148' in prompt:
        response_text = """
        PREGUNTA: ¿Qué técnica NO es recomendada para la elicitación de requisitos según ISO/IEC/IEEE 29148?
        OPCIONES:
        A. Entrevistas
        B. Observación
        C. Implementación directa
        D. Workshops
        RESPUESTA CORRECTA: C
        EXPLICACIÓN: La implementación directa sin análisis previo no es una técnica recomendada para elicitación de requisitos. ISO/IEC/IEEE 29148 promueve técnicas como entrevistas, workshops, observación, análisis de documentación y prototipos para obtener requisitos.
        """
    elif 'ISO 9241' in prompt:
        response_text = """
        PREGUNTA: ¿Qué concepto es central en ISO 9241?
        OPCIONES:
        A. Programación Orientada a Objetos
        B. Usabilidad
        C. Gestión de Bases de Datos
        D. Documentación Técnica
        RESPUESTA CORRECTA: B
        EXPLICACIÓN: La Usabilidad es el concepto central en ISO 9241, que se enfoca en la ergonomía de la interacción humano-sistema, estableciendo principios para interfaces efectivas, eficientes y satisfactorias.
        """
    else:
        response_text = """
        PREGUNTA: ¿Cuál es el propósito principal de los estándares ISO?
        OPCIONES:
        A. Generar ingresos para la organización ISO
        B. Establecer especificaciones para productos y servicios
        C. Obligar a las empresas a seguir reglas estrictas
        D. Limitar la innovación en las organizaciones
        RESPUESTA CORRECTA: B
        EXPLICACIÓN: El propósito principal de los estándares ISO es establecer especificaciones y directrices internacionalmente reconocidas para productos, servicios y sistemas, para asegurar calidad, seguridad y eficiencia.
        """
    
    # Simular la respuesta de Ollama
    response = {
        "model": "gpt-oss",
        "created_at": "2023-11-04T12:34:56Z",
        "response": response_text.strip(),
        "done": True
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='localhost', port=11434, debug=True)
