#!/usr/bin/env python3
"""Test rápido de 10 segundos para verificar LLM."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config
from src.llm import LLMClient

print("🚀 Test Rápido LLM...")
print(f"   Provider: {config.llm_provider}")

try:
    # Inicializar
    client = LLMClient(config)
    print("   ✅ Cliente inicializado")
    
    # Test simple
    response = client.invoke(
        "Di 'OK' si me entiendes",
        parse_json=False
    )
    print(f"   ✅ Respuesta: {response.strip()}")
    print("\n✅ ¡LLM FUNCIONA!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)
