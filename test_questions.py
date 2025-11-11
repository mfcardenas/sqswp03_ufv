import json
from app import get_fallback_question

# Script para probar la generación de preguntas sin Ollama
# Útil para verificar si las preguntas predefinidas funcionan correctamente

def test_fallback_questions():
    """Prueba la generación de preguntas predefinidas para cada estándar."""
    standards = [
        "ISO/IEC 25010:2023",
        "ISO/IEC/IEEE 29148", 
        "ISO 9241"
    ]
    
    print("Probando generación de preguntas fallback:\n")
    
    for standard in standards:
        print(f"Estándar: {standard}")
        print("-" * 50)
        
        # Genera 2 preguntas para cada estándar
        for i in range(2):
            question = get_fallback_question(standard)
            print(f"Pregunta {i+1}:")
            print(f"- Pregunta: {question['question']}")
            print(f"- Opciones:")
            for option in question['options']:
                print(f"  {option}")
            print(f"- Respuesta correcta: {question['correct_answer']}")
            print(f"- Explicación: {question['explanation'][:100]}...")
            print()
        
        print()

if __name__ == "__main__":
    test_fallback_questions()
