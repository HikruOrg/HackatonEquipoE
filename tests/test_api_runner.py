#!/usr/bin/env python3
"""Script para ejecutar los tests del API con verificación previa."""
import subprocess
import sys
import time
import requests
from pathlib import Path

def check_server():
    """Verificar si el servidor está corriendo."""
    try:
        response = requests.get("http://localhost:8000/", timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    print("🔍 Verificando estado del servidor...")
    
    if check_server():
        print("✅ Servidor activo en http://localhost:8000")
        print("\n🚀 Ejecutando tests del API...\n")
        
        # Ejecutar el script de tests desde el directorio de tests
        test_script = Path(__file__).parent / "test_api.py"
        subprocess.run([sys.executable, str(test_script)])
    else:
        print("❌ El servidor no está corriendo\n")
        print("Para ejecutar los tests, necesitas:")
        print("1️⃣  Abrir una nueva terminal")
        print("2️⃣  Activar el entorno virtual: .\\venv\\Scripts\\Activate.ps1")
        print("3️⃣  Iniciar el servidor: python run_server.py")
        print("4️⃣  Volver a esta terminal y ejecutar: python tests/test_api_runner.py")
        print("\nO ejecuta directamente: python tests/test_api.py (verás el error de conexión)")

if __name__ == "__main__":
    main()
