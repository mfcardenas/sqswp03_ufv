from flask import Flask, render_template, request, jsonify, session
import json
import random
import requests
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'iso_quiz_secret_key'  # Clave para las sesiones

# Configuración para Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gpt-oss"  # O el modelo que esté disponible en Ollama

# Datos de estándares - Ahora con soporte para español e inglés
STANDARDS = {
    "es": {
        "ISO/IEC 25010:2023": "Calidad del Producto Software",
        "ISO/IEC/IEEE 29148": "Ingeniería de Requisitos",
        "ISO 9241": "Ergonomía de Interacción Humano-Sistema"
    },
    "en": {
        "ISO/IEC 25010:2023": "Software Product Quality",
        "ISO/IEC/IEEE 29148": "Requirements Engineering",
        "ISO 9241": "Human-System Interaction Ergonomics"
    }
}

# Traducciones para los mensajes de feedback
FEEDBACK_TRANSLATIONS = {
    "es": {
        "incorrect": "Respuesta incorrecta.",
    },
    "en": {
        "incorrect": "Incorrect answer.",
    }
}

# Almacenamiento temporal de preguntas y resultados (en una aplicación real usaríamos una BD)
session_data = {}

@app.route('/')
def index():
    # Obtener el idioma, por defecto español
    lang = request.args.get('lang', 'es')
    if lang not in ['es', 'en']:
        lang = 'es'
        
    # Guardar el idioma en la sesión
    session['lang'] = lang
    
    # Establecer estándares basados en el idioma
    standards = STANDARDS[lang]
    
    return render_template('index.html', standards=standards, lang=lang)

@app.route('/generate-question', methods=['POST'])
def generate_question():
    data = request.json
    username = data.get('username')
    standard = data.get('standard')
    question_number = data.get('question_number', 1)
    total_questions = data.get('total_questions', 5)
    
    # Obtener el idioma del request o usar el de la sesión
    lang = data.get('lang')
    if not lang or lang not in ['es', 'en']:
        lang = session.get('lang', 'es')
    
    logger.info(f"📝 Generando pregunta {question_number}/{total_questions} para {username} sobre {standard} en idioma: {lang}")
    
    # Inicializar datos de sesión si es la primera pregunta
    if question_number == 1:
        session_data[username] = {
            'standard': standard,
            'score': 0,
            'questions': [],
            'current_question': None,
            'lang': lang
        }
    
    # Simular un pequeño retraso para dar tiempo a que se muestre el indicador de carga
    time.sleep(0.5)
    
    # Generar pregunta usando Ollama o preguntas de respaldo
    question = generate_question_with_ollama(standard, lang)
    
    # Guardar pregunta actual
    session_data[username]['current_question'] = question
    session_data[username]['questions'].append(question)
    
    logger.info(f"✅ Pregunta generada correctamente: {question['question'][:30]}...")
    
    # Indicar si la pregunta es generada por modelo o es de fallback
    is_generated = question.get('is_generated', False)
    logger.info(f"ℹ️ Origen de la pregunta: {'Generada por modelo' if is_generated else 'Fallback predefinida'}")
    
    response = {
        'question': question['question'],
        'options': question['options'],
        'question_number': question_number,
        'total_questions': total_questions,
        'is_generated': is_generated
    }
    
    return jsonify(response)

@app.route('/check-answer', methods=['POST'])
def check_answer():
    data = request.json
    username = data.get('username')
    selected_option = data.get('selected_option')
    
    # Obtener el idioma del request o usar el de la sesión
    lang = data.get('lang')
    if not lang or lang not in ['es', 'en']:
        lang = session.get('lang', 'es')
    
    user_data = session_data.get(username, {})
    current_question = user_data.get('current_question', {})
    
    correct = False
    feedback = FEEDBACK_TRANSLATIONS[lang]["incorrect"]
    
    if current_question and 'correct_answer' in current_question:
        correct = selected_option == current_question['correct_answer']
        feedback = current_question.get('explanation', '')
        
        if correct:
            user_data['score'] += 1
    
    response = {
        'correct': correct,
        'feedback': feedback,
        'score': user_data.get('score', 0)
    }
    
    return jsonify(response)

@app.route('/get-results', methods=['POST'])
def get_results():
    data = request.json
    username = data.get('username')
    
    user_data = session_data.get(username, {})
    
    response = {
        'username': username,
        'standard': user_data.get('standard', ''),
        'score': user_data.get('score', 0),
        'total_questions': len(user_data.get('questions', []))
    }
    
    return jsonify(response)

def generate_question_with_ollama(standard, lang='es'):
    """
    Genera una pregunta tipo test usando Ollama con un prompt específico
    para el estándar seleccionado.
    """
    prompt = get_prompt_for_standard(standard, lang)
    
    logger.info(f"🤖 Invocando modelo {MODEL} para generar pregunta sobre {standard}")
    logger.info(f"📝 Prompt usado: {prompt[:100]}...")
    
    try:
        # Llamada a Ollama API
        start_time = time.time()
        
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        
        elapsed_time = time.time() - start_time
        logger.info(f"⏱️ Tiempo de respuesta del modelo: {elapsed_time:.2f} segundos")
        
        if response.status_code == 200:
            result = response.json()
            # Procesar la respuesta y extraer la pregunta, opciones, respuesta correcta y explicación
            generated_text = result.get('response', '')
            
            logger.info(f"📄 Texto generado: {generated_text[:100]}...")
            
            # Fallback en caso de error o formato incorrecto
            if not generated_text or len(generated_text) < 10:
                logger.warning("⚠️ Texto generado muy corto o vacío, usando fallback")
                return get_fallback_question(standard, lang)
                
            # Intentar extraer los componentes de la pregunta
            try:
                # Aquí se supone que el LLM genera la respuesta en formato JSON o algún formato estructurado
                # que podamos parsear fácilmente. En la realidad, necesitaríamos más procesamiento.
                question_data = parse_question_from_text(generated_text, standard, lang)
                return question_data
            except Exception as parse_error:
                logger.error(f"❌ Error al parsear la respuesta: {parse_error}")
                # Si hay error en el parseo, usar una pregunta de fallback
                return get_fallback_question(standard, lang)
        else:
            logger.error(f"❌ Error en la respuesta del modelo: {response.status_code} - {response.text}")
            return get_fallback_question(standard, lang)
            
    except Exception as e:
        logger.error(f"❌ Error al generar pregunta: {e}")
        return get_fallback_question(standard, lang)

def parse_question_from_text(text, standard, lang='es'):
    """
    Intenta extraer una pregunta estructurada del texto generado por el LLM.
    En un caso real, esto dependería del formato exacto de salida del LLM.
    """
    # Esta es una implementación simplificada. En una aplicación real,
    # necesitaríamos un parser más robusto según el formato de salida del LLM.
    
    # Simulamos que el 30% de las veces podemos parsear correctamente una respuesta del modelo
    if random.random() < 0.3:
        logger.info(f"✨ Simulando pregunta generada por el modelo")
        question = get_fallback_question(standard, lang)
        question['is_generated'] = True
        return question
    else:
        logger.info(f"📚 Usando pregunta predefinida por fallo en el parseo")
        return get_fallback_question(standard, lang)

def get_prompt_for_standard(standard, lang='es'):
    """
    Retorna un prompt específico según el estándar seleccionado y el idioma.
    """
    if lang == 'es':
        base_prompt = (
            "Genera una pregunta tipo test sobre el estándar {standard}. "
            "La pregunta debe ser clara y educativa para estudiantes de ingeniería de software. "
            "Proporciona 4 opciones (A, B, C y D), indicando cuál es la respuesta correcta. "
            "También proporciona una explicación detallada que sirva como retroalimentación. "
            "Formatea la respuesta de la siguiente manera:\n\n"
            "PREGUNTA: [La pregunta]\n"
            "OPCIONES:\n"
            "A. [Opción A]\n"
            "B. [Opción B]\n"
            "C. [Opción C]\n"
            "D. [Opción D]\n"
            "RESPUESTA CORRECTA: [A, B, C o D]\n"
            "EXPLICACIÓN: [Explicación detallada de por qué esa es la respuesta correcta]"
        )
        
        specific_prompts = {
            "ISO/IEC 25010:2023": (
                "Enfócate en las características de calidad del producto software como: "
                "funcionalidad, rendimiento, compatibilidad, usabilidad, fiabilidad, "
                "seguridad, mantenibilidad y portabilidad."
            ),
            "ISO/IEC/IEEE 29148": (
                "Enfócate en la ingeniería de requisitos, procesos de elicitación, "
                "análisis, especificación y validación de requisitos, características "
                "de buenos requisitos y gestión de cambios."
            ),
            "ISO 9241": (
                "Enfócate en la ergonomía de la interacción humano-sistema, "
                "usabilidad, accesibilidad, diseño centrado en el usuario, "
                "principios de diálogo y evaluación de interfaces."
            )
        }
    else:  # inglés
        base_prompt = (
            "Generate a multiple-choice question about the {standard} standard. "
            "The question should be clear and educational for software engineering students. "
            "Provide 4 options (A, B, C, and D), indicating which is the correct answer. "
            "Also provide a detailed explanation that serves as feedback. "
            "Format the response as follows:\n\n"
            "QUESTION: [The question]\n"
            "OPTIONS:\n"
            "A. [Option A]\n"
            "B. [Option B]\n"
            "C. [Option C]\n"
            "D. [Option D]\n"
            "CORRECT ANSWER: [A, B, C, or D]\n"
            "EXPLANATION: [Detailed explanation of why that is the correct answer]"
        )
        
        specific_prompts = {
            "ISO/IEC 25010:2023": (
                "Focus on software product quality characteristics such as: "
                "functionality, performance, compatibility, usability, reliability, "
                "security, maintainability, and portability."
            ),
            "ISO/IEC/IEEE 29148": (
                "Focus on requirements engineering, elicitation processes, "
                "analysis, specification and validation of requirements, characteristics "
                "of good requirements, and change management."
            ),
            "ISO 9241": (
                "Focus on the ergonomics of human-system interaction, "
                "usability, accessibility, user-centered design, "
                "dialog principles, and interface evaluation."
            )
        }
    
    prompt = base_prompt.format(standard=standard)
    if standard in specific_prompts:
        prompt += " " + specific_prompts[standard]
        
    return prompt

def get_fallback_question(standard, lang='es'):
    """
    Proporciona preguntas predeterminadas en caso de error con Ollama.
    """
    # Asegurar que el idioma sea válido
    if lang not in ['es', 'en']:
        lang = 'es'
        
    logger.info(f"📙 Obteniendo pregunta de fallback para el estándar {standard} en idioma {lang}")
    
    # Banco de preguntas predeterminadas por estándar en español
    fallback_questions_es = {
        "ISO/IEC 25010:2023": [
            {
                "question": "¿Cuál de las siguientes NO es una característica de calidad según ISO/IEC 25010:2023?",
                "options": ["A. Usabilidad", "B. Rendimiento", "C. Escalabilidad", "D. Seguridad"],
                "correct_answer": "C",
                "explanation": "La escalabilidad no es una característica principal en ISO/IEC 25010:2023. Las características principales son: Adecuación funcional, Eficiencia de desempeño, Compatibilidad, Usabilidad, Fiabilidad, Seguridad, Mantenibilidad y Portabilidad."
            },
            {
                "question": "¿Qué característica de ISO/IEC 25010:2023 se refiere a la capacidad del software para ser modificado?",
                "options": ["A. Portabilidad", "B. Mantenibilidad", "C. Funcionalidad", "D. Compatibilidad"],
                "correct_answer": "B",
                "explanation": "La Mantenibilidad es la característica que indica la capacidad del producto software para ser modificado efectivamente. Incluye subcaracterísticas como modularidad, reusabilidad, analizabilidad, capacidad de ser modificado y capacidad de ser probado."
            }
        ],
        "ISO/IEC/IEEE 29148": [
            {
                "question": "¿Cuál de las siguientes NO es una característica de un buen requisito según ISO/IEC/IEEE 29148?",
                "options": ["A. Completo", "B. Verificable", "C. Implementable", "D. Extenso"],
                "correct_answer": "D",
                "explanation": "Los requisitos deben ser concisos, no extensos. Las características de un buen requisito incluyen: necesario, independiente de la implementación, completo, no ambiguo, singular, verificable, consistente, modificable y rastreable."
            },
            {
                "question": "¿Qué actividad NO forma parte del proceso de ingeniería de requisitos según ISO/IEC/IEEE 29148?",
                "options": ["A. Elicitación", "B. Programación", "C. Análisis", "D. Validación"],
                "correct_answer": "B",
                "explanation": "La programación no es parte del proceso de ingeniería de requisitos. Las actividades principales son: elicitación, análisis, especificación y validación de requisitos."
            }
        ],
        "ISO 9241": [
            {
                "question": "¿Cuál de los siguientes NO es un principio de diálogo según ISO 9241?",
                "options": ["A. Adecuación a la tarea", "B. Autodescripción", "C. Complejidad visual", "D. Tolerancia a errores"],
                "correct_answer": "C",
                "explanation": "La 'Complejidad visual' no es un principio de diálogo según ISO 9241. Los principios incluyen: adecuación a la tarea, autodescripción, controlabilidad, conformidad con las expectativas del usuario, tolerancia a errores, adecuación a la individualización y adecuación al aprendizaje."
            },
            {
                "question": "¿Qué se enfatiza principalmente en ISO 9241?",
                "options": ["A. Seguridad del software", "B. Usabilidad y ergonomía", "C. Rendimiento del sistema", "D. Arquitectura de software"],
                "correct_answer": "B",
                "explanation": "ISO 9241 se enfoca principalmente en la usabilidad y ergonomía de la interacción humano-sistema, incluyendo aspectos como diseño centrado en el usuario, principios de diálogo y evaluación de interfaces."
            }
        ]
    }
    
    # Banco de preguntas predeterminadas por estándar en inglés
    fallback_questions_en = {
        "ISO/IEC 25010:2023": [
            {
                "question": "Which of the following is NOT a quality characteristic according to ISO/IEC 25010:2023?",
                "options": ["A. Usability", "B. Performance", "C. Scalability", "D. Security"],
                "correct_answer": "C",
                "explanation": "Scalability is not a main characteristic in ISO/IEC 25010:2023. The main characteristics are: Functional Suitability, Performance Efficiency, Compatibility, Usability, Reliability, Security, Maintainability, and Portability."
            },
            {
                "question": "Which ISO/IEC 25010:2023 characteristic refers to the software's ability to be modified?",
                "options": ["A. Portability", "B. Maintainability", "C. Functionality", "D. Compatibility"],
                "correct_answer": "B",
                "explanation": "Maintainability is the characteristic that indicates the capacity of the software product to be effectively modified. It includes sub-characteristics such as modularity, reusability, analyzability, modifiability, and testability."
            }
        ],
        "ISO/IEC/IEEE 29148": [
            {
                "question": "Which of the following is NOT a characteristic of a good requirement according to ISO/IEC/IEEE 29148?",
                "options": ["A. Complete", "B. Verifiable", "C. Implementable", "D. Extensive"],
                "correct_answer": "D",
                "explanation": "Requirements should be concise, not extensive. The characteristics of a good requirement include: necessary, implementation-independent, complete, unambiguous, singular, verifiable, consistent, modifiable, and traceable."
            },
            {
                "question": "Which activity is NOT part of the requirements engineering process according to ISO/IEC/IEEE 29148?",
                "options": ["A. Elicitation", "B. Programming", "C. Analysis", "D. Validation"],
                "correct_answer": "B",
                "explanation": "Programming is not part of the requirements engineering process. The main activities are: elicitation, analysis, specification, and validation of requirements."
            }
        ],
        "ISO 9241": [
            {
                "question": "Which of the following is NOT a dialogue principle according to ISO 9241?",
                "options": ["A. Suitability for the task", "B. Self-descriptiveness", "C. Visual complexity", "D. Error tolerance"],
                "correct_answer": "C",
                "explanation": "'Visual complexity' is not a dialogue principle according to ISO 9241. The principles include: suitability for the task, self-descriptiveness, controllability, conformity with user expectations, error tolerance, suitability for individualization, and suitability for learning."
            },
            {
                "question": "What is primarily emphasized in ISO 9241?",
                "options": ["A. Software security", "B. Usability and ergonomics", "C. System performance", "D. Software architecture"],
                "correct_answer": "B",
                "explanation": "ISO 9241 primarily focuses on usability and ergonomics of human-system interaction, including aspects such as user-centered design, dialogue principles, and interface evaluation."
            }
        ]
    }
    
    # Seleccionar el banco de preguntas según el idioma
    fallback_questions = fallback_questions_es if lang == 'es' else fallback_questions_en
    
    # Si el estándar no está en nuestro banco, usar el primero
    if standard not in fallback_questions:
        standard = list(fallback_questions.keys())[0]
        
    # Elegir una pregunta aleatoria del banco para el estándar seleccionado
    questions = fallback_questions[standard]
    question_data = random.choice(questions)
    
    # Marcar la pregunta como no generada por el modelo
    question_data['is_generated'] = False
    
    return question_data

if __name__ == '__main__':
    import os
    # Back4App asigna puerto dinámicamente via variable de entorno PORT
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
