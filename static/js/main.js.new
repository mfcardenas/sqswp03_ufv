// Variables globales
let currentQuestionNumber = 1;
let totalQuestions = 5;
let currentScore = 0;
let username = '';
let selectedStandard = '';
let currentLang = 'es'; // Idioma por defecto: español
let isAnswering = false; // Para controlar el flujo de contestar preguntas

// Elementos DOM
let startSection, quizSection, resultsSection, startForm, questionText, optionsContainer;
let feedbackContainer, feedbackText, nextButton, restartButton, languageSelect;

// Inicializar elementos DOM cuando el documento esté listo
function initDOMElements() {
    startSection = document.getElementById('start-section');
    quizSection = document.getElementById('quiz-section');
    resultsSection = document.getElementById('results-section');
    startForm = document.getElementById('start-form');
    questionText = document.getElementById('question-text');
    optionsContainer = document.getElementById('options-container');
    feedbackContainer = document.getElementById('feedback-container');
    feedbackText = document.getElementById('feedback-text');
    nextButton = document.getElementById('next-button');
    restartButton = document.getElementById('restart-button');
    languageSelect = document.getElementById('language-select');
    
    // Verificar que todos los elementos esenciales existan
    if (!startSection || !quizSection || !resultsSection || !startForm || 
        !questionText || !optionsContainer || !feedbackContainer || 
        !feedbackText || !nextButton || !restartButton || !languageSelect) {
        console.error("No se pudieron inicializar todos los elementos DOM", {
            startSection, quizSection, resultsSection, startForm, 
            questionText, optionsContainer, feedbackContainer,
            feedbackText, nextButton, restartButton, languageSelect
        });
    } else {
        console.log("Elementos DOM inicializados correctamente");
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM cargado, inicializando elementos...");
    initDOMElements();
    
    startForm.addEventListener('submit', startQuiz);
    nextButton.addEventListener('click', loadNextQuestion);
    restartButton.addEventListener('click', resetQuiz);
    languageSelect.addEventListener('change', changeLanguage);
    
    // Obtener el idioma de la URL (si existe)
    const urlParams = new URLSearchParams(window.location.search);
    const langParam = urlParams.get('lang');
    
    // Cargar el idioma guardado en localStorage o de la URL
    if (langParam && (langParam === 'es' || langParam === 'en')) {
        currentLang = langParam;
        localStorage.setItem('language', currentLang);
    } else if (localStorage.getItem('language')) {
        currentLang = localStorage.getItem('language');
    }
    
    // Establecer el selector al idioma actual
    languageSelect.value = currentLang;
    
    // Aplicar traducciones al cargar la página
    applyTranslations();
    console.log("Inicialización completada");
});

// Función para cambiar el idioma
function changeLanguage(e) {
    currentLang = e.target.value;
    localStorage.setItem('language', currentLang);
    
    // Actualizar traducciones en la interfaz
    applyTranslations();
    
    // Recargar la página con el parámetro de idioma para actualizar los estándares desde el backend
    // Solo si estamos en la página de inicio
    if (!startSection.classList.contains('hidden')) {
        window.location.href = `/?lang=${currentLang}`;
    }
}

// Función para aplicar traducciones según el idioma seleccionado
function applyTranslations() {
    console.log(`Aplicando traducciones para el idioma: ${currentLang}`);
    
    // Título de la página
    document.getElementById('page-title').textContent = translations[currentLang].pageTitle;
    
    // Encabezado
    document.getElementById('header-title').textContent = translations[currentLang].headerTitle;
    document.getElementById('header-subtitle').textContent = translations[currentLang].headerSubtitle;
    
    // Selector de idioma
    document.getElementById('language-label').textContent = translations[currentLang].languageLabel;
    
    // Sección de inicio
    document.getElementById('start-title').textContent = translations[currentLang].startTitle;
    document.getElementById('username-label').textContent = translations[currentLang].usernameLabel;
    document.getElementById('standard-label').textContent = translations[currentLang].standardLabel;
    document.getElementById('select-standard-option').textContent = translations[currentLang].selectStandardOption;
    document.getElementById('questions-count-label').textContent = translations[currentLang].questionsCountLabel;
    
    // Actualizar textos de las opciones del selector de preguntas
    const questionsOptions = document.querySelectorAll('#questions-count option');
    questionsOptions[0].textContent = `5 ${translations[currentLang].questionsOption}`;
    questionsOptions[1].textContent = `10 ${translations[currentLang].questionsOption}`;
    
    document.getElementById('start-button').textContent = translations[currentLang].startButton;
    
    // Sección de preguntas
    document.getElementById('user-label').textContent = translations[currentLang].userLabel;
    document.getElementById('standard-label').textContent = translations[currentLang].standardLabel;
    document.getElementById('question-label').textContent = translations[currentLang].questionLabel;
    document.getElementById('of-label').textContent = translations[currentLang].of;
    document.getElementById('score-label').textContent = translations[currentLang].scoreLabel;
    document.getElementById('next-button').textContent = 
        currentQuestionNumber >= totalQuestions 
            ? translations[currentLang].viewResultsButton 
            : translations[currentLang].nextButton;
    
    // Sección de resultados
    document.getElementById('results-title').textContent = translations[currentLang].resultsTitle;
    document.getElementById('final-score-label').textContent = translations[currentLang].finalScore;
    document.getElementById('of-label-2').textContent = translations[currentLang].of;
    document.getElementById('restart-button').textContent = translations[currentLang].restartButton;
    
    // Pie de página
    document.getElementById('footer-text').textContent = translations[currentLang].footerText;
}

// Función para actualizar las descripciones de los estándares según el idioma
function updateStandardsDescription() {
    // En la implementación actual, los estándares se reciben del backend
    // y la recarga de la página con el parámetro lang se encarga de actualizarlos
    // Esta función queda como referencia para futuras mejoras o implementaciones del lado del cliente
    console.log("Estándares actualizados para el idioma:", currentLang);
}

// Función para iniciar el quiz
function startQuiz(e) {
    e.preventDefault();
    
    // Obtener datos del formulario
    username = document.getElementById('username').value.trim();
    selectedStandard = document.getElementById('standard').value;
    totalQuestions = parseInt(document.getElementById('questions-count').value);
    
    if (!username || !selectedStandard) {
        alert(translations[currentLang].formValidationAlert);
        return;
    }
    
    // Actualizar información de usuario
    document.getElementById('username-value').textContent = username;
    document.getElementById('standard-value').textContent = selectedStandard;
    
    // Ocultar sección de inicio y mostrar sección de quiz
    startSection.classList.add('hidden');
    quizSection.classList.remove('hidden');
    
    // Cargar primera pregunta
    loadQuestion();
}

// Función para ocultar el indicador de carga
function hideLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.classList.add('hidden');
        console.log("Indicador de carga ocultado correctamente");
    } else {
        console.warn("No se encontró el elemento del indicador de carga para ocultar");
    }
}

// Función para mostrar el indicador de carga
function showLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.classList.remove('hidden');
        console.log("Indicador de carga mostrado correctamente");
        const loadingText = document.getElementById('loading-text');
        if (loadingText && translations[currentLang]) {
            loadingText.textContent = translations[currentLang].loadingText;
        }
    } else {
        console.warn("No se encontró el elemento del indicador de carga para mostrar");
    }
}

// Función para cargar una pregunta
function loadQuestion() {
    // Evitar múltiples operaciones durante la carga
    isAnswering = false;
    
    console.log(`Cargando pregunta ${currentQuestionNumber} de ${totalQuestions} en idioma ${currentLang}`);
    
    // Actualizar progreso con IDs correctos para traducciones
    const questionProgress = document.getElementById('question-progress');
    if (questionProgress) {
        questionProgress.innerHTML = 
            `<span id="question-label">${translations[currentLang].questionLabel}</span> ${currentQuestionNumber} 
             <span id="of-label">${translations[currentLang].of}</span> ${totalQuestions}`;
    }
    
    const scoreDisplay = document.getElementById('score-display');
    if (scoreDisplay) {
        scoreDisplay.innerHTML = 
            `<span id="score-label">${translations[currentLang].scoreLabel}</span> ${currentScore}`;
    }
    
    // Ocultar feedback de pregunta anterior
    if (feedbackContainer) {
        feedbackContainer.classList.add('hidden');
    }
    
    // Ocultar el indicador de origen de la pregunta
    const questionSource = document.getElementById('question-source');
    if (questionSource) {
        questionSource.classList.add('hidden');
    }
    
    // Mostrar el indicador de carga
    showLoadingIndicator();
    
    // Ocultar el texto de la pregunta y las opciones mientras se carga
    if (questionText) {
        questionText.textContent = '';
    }
    if (optionsContainer) {
        optionsContainer.innerHTML = '';
    }
    
    // Verificar que los elementos DOM existan antes de continuar
    if (!questionText || !optionsContainer) {
        console.error("Elementos DOM de preguntas no encontrados. Asegúrese de que la página está completamente cargada.");
        hideLoadingIndicator();
        return;
    }
    
    // Petición al servidor para obtener pregunta
    fetch('/generate-question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            standard: selectedStandard,
            question_number: currentQuestionNumber,
            total_questions: totalQuestions,
            lang: currentLang
        })
    })
    .then(response => {
        console.log(`Respuesta recibida del servidor: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log("Datos de pregunta recibidos:", data);
        
        // Ocultar el indicador de carga
        hideLoadingIndicator();
        
        // Mostrar pregunta
        if (data.question && questionText) {
            questionText.textContent = data.question;
            
            // Mostrar el origen de la pregunta
            const questionSource = document.getElementById('question-source');
            const sourceIcon = document.getElementById('source-icon');
            const sourceText = document.getElementById('source-text');
            
            if (questionSource && sourceIcon && sourceText) {
                if (data.is_generated) {
                    sourceIcon.textContent = '🤖';
                    sourceText.textContent = translations[currentLang].sourceAI;
                } else {
                    sourceIcon.textContent = '📚';
                    sourceText.textContent = translations[currentLang].sourceDefault;
                }
                
                questionSource.classList.remove('hidden');
            } else {
                console.warn("No se encontraron elementos para mostrar el origen de la pregunta");
            }
        } else {
            if (questionText) {
                questionText.textContent = translations[currentLang].exampleQuestion || '¿Pregunta de ejemplo?';
                console.log("Usando pregunta de ejemplo en", currentLang);
            } else {
                console.error("Elemento questionText no encontrado");
            }
        }
        
        // Generar opciones
        if (optionsContainer) {
            optionsContainer.innerHTML = '';
            
            if (data.options && data.options.length > 0) {
                data.options.forEach((option, index) => {
                    const optionElement = document.createElement('div');
                    optionElement.classList.add('option');
                    optionElement.textContent = option;
                    optionElement.dataset.option = option.charAt(0); // Extraer A, B, C o D
                    optionElement.addEventListener('click', selectOption);
                    optionsContainer.appendChild(optionElement);
                });
            } else {
                console.log("No hay opciones disponibles para esta pregunta");
            }
        } else {
            console.error("Elemento optionsContainer no encontrado");
        }
        
        // Actualizar el texto del botón según el progreso
        if (nextButton) {
            nextButton.textContent = 
                currentQuestionNumber >= totalQuestions 
                    ? translations[currentLang].viewResultsButton 
                    : translations[currentLang].nextButton;
        } else {
            console.warn("Elemento nextButton no encontrado");
        }
    })
    .catch(error => {
        console.error('Error al cargar pregunta:', error);
        
        // Ocultar el indicador de carga
        hideLoadingIndicator();
        
        if (questionText) {
            questionText.textContent = translations[currentLang].loadQuestionError;
        }
    });
}

// Función para seleccionar una opción
function selectOption(e) {
    // Evitar selecciones múltiples
    if (feedbackContainer.classList.contains('hidden') && !isAnswering) {
        isAnswering = true; // Activar estado de respuesta
        console.log("Seleccionando opción");
        
        const selectedOption = e.target;
        
        // Marcar opción seleccionada
        document.querySelectorAll('.option').forEach(option => {
            option.classList.remove('selected');
        });
        selectedOption.classList.add('selected');
        
        // Verificar respuesta
        checkAnswer(selectedOption.dataset.option);
    } else {
        console.log("Ignorando clic: ya se está respondiendo o el feedback está visible");
    }
}

// Función para verificar la respuesta
function checkAnswer(selectedOption) {
    console.log(`Verificando respuesta: ${selectedOption} en idioma ${currentLang}`);
    
    fetch('/check-answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            selected_option: selectedOption,
            lang: currentLang
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Respuesta del servidor:", data);
        
        // Actualizar puntuación
        currentScore = data.score;
        const scoreDisplay = document.getElementById('score-display');
        if (scoreDisplay) {
            scoreDisplay.innerHTML = 
                `<span id="score-label">${translations[currentLang].scoreLabel}</span> ${currentScore}`;
        }
        
        // Marcar opciones correctas/incorrectas
        const options = document.querySelectorAll('.option');
        options.forEach(option => {
            if (option.classList.contains('selected')) {
                if (data.correct) {
                    option.classList.add('correct');
                } else {
                    option.classList.add('incorrect');
                }
            }
        });
        
        // Mostrar feedback
        if (feedbackText && feedbackContainer) {
            feedbackText.innerHTML = data.feedback;
            feedbackContainer.classList.remove('hidden');
        }
        
        // Si es la última pregunta, cambiar texto del botón
        if (currentQuestionNumber >= totalQuestions && nextButton) {
            nextButton.textContent = translations[currentLang].viewResultsButton;
        }
    })
    .catch(error => {
        console.error('Error al verificar respuesta:', error);
        isAnswering = false; // Permitir intentar de nuevo si hay error
    });
}

// Función para cargar la siguiente pregunta
function loadNextQuestion() {
    console.log(`Cargando siguiente pregunta. Actual: ${currentQuestionNumber}, Total: ${totalQuestions}`);
    
    // Si es la última pregunta, mostrar resultados
    if (currentQuestionNumber >= totalQuestions) {
        console.log("Última pregunta completada, mostrando resultados");
        showResults();
        return;
    }
    
    // Incrementar número de pregunta y cargar siguiente
    currentQuestionNumber++;
    loadQuestion();
}

// Función para mostrar resultados
function showResults() {
    console.log("Mostrando resultados finales");
    isAnswering = false; // Resetear estado

    fetch('/get-results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            lang: currentLang
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Resultados recibidos:", data);
        
        // Actualizar sección de resultados
        const finalScoreElement = document.getElementById('final-score');
        if (finalScoreElement) {
            finalScoreElement.innerHTML = 
                `<span id="final-score-label">${translations[currentLang].finalScore}</span> ${data.score} 
                 <span id="of-label-2">${translations[currentLang].of}</span> ${data.total_questions}`;
        }
        
        const percentage = Math.round((data.score / data.total_questions) * 100);
        const percentageScore = document.getElementById('percentage-score');
        if (percentageScore) {
            percentageScore.textContent = `${percentage}%`;
        }
        
        // Mensaje de feedback según puntuación
        const feedbackMessage = document.getElementById('feedback-message');
        if (feedbackMessage) {
            if (percentage >= 80) {
                feedbackMessage.textContent = translations[currentLang].feedbackExcellent;
            } else if (percentage >= 60) {
                feedbackMessage.textContent = translations[currentLang].feedbackGood;
            } else if (percentage >= 40) {
                feedbackMessage.textContent = translations[currentLang].feedbackAverage;
            } else {
                feedbackMessage.textContent = translations[currentLang].feedbackPoor;
            }
        }
        
        // Mostrar sección de resultados
        if (quizSection && resultsSection) {
            quizSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');
        }
    })
    .catch(error => {
        console.error('Error al obtener resultados:', error);
    });
}

// Función para reiniciar el quiz
function resetQuiz() {
    // Reiniciar variables
    currentQuestionNumber = 1;
    currentScore = 0;
    
    // Volver a la pantalla de inicio
    if (resultsSection && startSection) {
        resultsSection.classList.add('hidden');
        startSection.classList.remove('hidden');
    }
}
