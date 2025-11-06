#!/usr/bin/env python3
"""Script para verificar la conexión con el LLM."""
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config
from src.llm import LLMClient

def test_llm_connection():
    """Prueba la conexión con el LLM."""
    print("=" * 70)
    print("🧪 Test de Conexión con LLM")
    print("=" * 70)
    print()
    
    # 1. Mostrar configuración
    print("📋 Configuración:")
    print(f"   Provider: {config.llm_provider}")
    
    if config.llm_provider == "openai":
        print(f"   Model: {config.openai_model}")
        api_key = config.openai_api_key
        key_display = f"{api_key[:10]}...{api_key[-4:]}" if api_key else "❌ NO CONFIGURADA"
        print(f"   API Key: {key_display}")
    elif config.llm_provider == "gemini":
        print(f"   Model: {config.gemini_model}")
        api_key = config.google_api_key
        key_display = f"{api_key[:10]}...{api_key[-4:]}" if api_key else "❌ NO CONFIGURADA"
        print(f"   API Key: {key_display}")
    elif config.llm_provider == "anthropic":
        print(f"   Model: {config.anthropic_model}")
        api_key = config.anthropic_api_key
        key_display = f"{api_key[:10]}...{api_key[-4:]}" if api_key else "❌ NO CONFIGURADA"
        print(f"   API Key: {key_display}")
    elif config.llm_provider == "ollama":
        print(f"   Model: {config.ollama_model}")
        print(f"   Base URL: {config.ollama_base_url}")
    
    print(f"   Temperature: {config.llm_temperature}")
    print(f"   Max Tokens: {config.llm_max_tokens}")
    print(f"   Timeout: {config.llm_timeout}s")
    print()
    
    # 2. Validar configuración
    print("🔍 Validando configuración...")
    try:
        config.validate()
        print("   ✅ Configuración válida")
    except ValueError as e:
        print(f"   ❌ Error de configuración: {e}")
        return False
    print()
    
    # 3. Inicializar cliente LLM
    print("🔌 Inicializando cliente LLM...")
    try:
        llm_client = LLMClient(config)
        print("   ✅ Cliente LLM inicializado")
    except Exception as e:
        print(f"   ❌ Error al inicializar: {e}")
        return False
    print()
    
    # 4. Test simple de texto
    print("📝 Test 1: Respuesta de texto simple")
    print("   Prompt: '¿Cuál es la capital de España?'")
    try:
        start_time = time.time()
        response = llm_client.invoke(
            "Responde en una sola palabra: ¿Cuál es la capital de España?",
            parse_json=False
        )
        elapsed = time.time() - start_time
        
        print(f"   ✅ Respuesta recibida en {elapsed:.2f}s")
        print(f"   📄 Respuesta: {response.strip()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    print()
    
    # 5. Test de respuesta JSON
    print("📊 Test 2: Respuesta JSON estructurada")
    json_prompt = """
Analiza el siguiente perfil de candidato y responde en formato JSON:

Candidato: Juan Pérez
Experiencia: 5 años en Python, 3 años en FastAPI
Educación: Ingeniería en Computación

Responde SOLO con JSON en este formato:
{
    "nombre": "nombre del candidato",
    "años_experiencia": número,
    "tecnologias": ["tech1", "tech2"],
    "nivel": "junior/mid/senior"
}
"""
    print("   Prompt: Análisis de perfil de candidato")
    try:
        start_time = time.time()
        response = llm_client.invoke(json_prompt, parse_json=True)
        elapsed = time.time() - start_time
        
        print(f"   ✅ JSON recibido en {elapsed:.2f}s")
        print(f"   📄 Respuesta:")
        import json
        print(json.dumps(response, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"   ⚠️  Advertencia: {e}")
        print("   (Algunos modelos pueden tener problemas con JSON en primera prueba)")
    print()
    
    # 6. Test de análisis de matching
    print("🎯 Test 3: Análisis de matching (simplificado)")
    matching_prompt = """
Compara este candidato con los requisitos del trabajo:

CANDIDATO:
- 5 años de experiencia en Python
- Conocimiento de FastAPI y Django
- Experiencia en bases de datos SQL

REQUISITOS:
- Python (obligatorio)
- FastAPI (obligatorio)
- 3+ años de experiencia

Responde SOLO en formato JSON:
{
    "match_score": 0.0-1.0,
    "cumple_requisitos": true/false,
    "razones": ["razón 1", "razón 2"]
}
"""
    print("   Prompt: Análisis de matching candidato-trabajo")
    try:
        start_time = time.time()
        response = llm_client.invoke(matching_prompt, parse_json=True)
        elapsed = time.time() - start_time
        
        print(f"   ✅ Análisis completado en {elapsed:.2f}s")
        print(f"   📄 Resultado:")
        import json
        print(json.dumps(response, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"   ⚠️  Advertencia: {e}")
        print("   (Algunos modelos pueden necesitar ajustes en el formato)")
    print()
    
    # Resumen final
    print("=" * 70)
    print("✅ ¡CONEXIÓN CON LLM EXITOSA!")
    print("=" * 70)
    print()
    print("El backend puede comunicarse correctamente con el LLM.")
    print("Puedes iniciar el servidor con: python run_server.py")
    print()
    
    return True


def main():
    """Run LLM connection test."""
    try:
        success = test_llm_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
