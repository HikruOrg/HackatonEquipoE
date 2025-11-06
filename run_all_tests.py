#!/usr/bin/env python3
"""
Script para ejecutar todos los tests del backend.
Ejecuta verificación de configuración, tests de LLM y tests de API.
"""

import sys
import subprocess
import time
from pathlib import Path

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def run_test(test_name, test_path):
    """Ejecuta un test y retorna True si fue exitoso."""
    print_header(f"Ejecutando: {test_name}")
    print_info(f"Script: {test_path}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_path)],
            capture_output=False,
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        if result.returncode == 0:
            print_success(f"{test_name} completado exitosamente\n")
            return True
        else:
            print_error(f"{test_name} falló con código {result.returncode}\n")
            return False
            
    except subprocess.TimeoutExpired:
        print_error(f"{test_name} excedió el tiempo límite (5 minutos)\n")
        return False
    except Exception as e:
        print_error(f"{test_name} falló con error: {e}\n")
        return False

def main():
    print_header("🧪 SUITE COMPLETA DE TESTS - BACKEND")
    
    tests_dir = Path(__file__).parent / "tests"
    
    # Lista de tests a ejecutar en orden
    tests = [
        ("1️⃣  Verificación de Configuración", tests_dir / "verify_setup.py"),
        ("2️⃣  Test LLM - Conexión Rápida", tests_dir / "test_llm_quick.py"),
        ("3️⃣  Test LLM - Conexión Completa", tests_dir / "test_llm_connection.py"),
        ("4️⃣  Test API - Endpoints Principales", tests_dir / "test_api.py"),
        ("5️⃣  Test API - Procesamiento PDF Resume", tests_dir / "test_api_pdf_resume.py"),
    ]
    
    results = {}
    start_time = time.time()
    
    # Ejecutar cada test
    for test_name, test_path in tests:
        if not test_path.exists():
            print_error(f"Test no encontrado: {test_path}")
            results[test_name] = False
            continue
        
        results[test_name] = run_test(test_name, test_path)
        time.sleep(1)  # Pequeña pausa entre tests
    
    # Resumen final
    elapsed_time = time.time() - start_time
    print_header("📊 RESUMEN DE RESULTADOS")
    
    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed
    
    print(f"\n{Colors.BOLD}Tests ejecutados: {len(results)}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓ Exitosos: {passed}{Colors.ENDC}")
    print(f"{Colors.FAIL}✗ Fallidos: {failed}{Colors.ENDC}")
    print(f"\n{Colors.OKCYAN}⏱️  Tiempo total: {elapsed_time:.2f} segundos{Colors.ENDC}\n")
    
    # Detalle de resultados
    print(f"{Colors.BOLD}Detalle:{Colors.ENDC}")
    for test_name, success in results.items():
        status = f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}" if success else f"{Colors.FAIL}✗ FAIL{Colors.ENDC}"
        print(f"  {status}  {test_name}")
    
    print()
    
    # Retornar código de salida apropiado
    if failed == 0:
        print_success("¡Todos los tests pasaron exitosamente! 🎉")
        return 0
    else:
        print_error(f"{failed} test(s) fallaron. Revisar logs arriba.")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print_error("\n\nTests interrumpidos por el usuario")
        sys.exit(130)
    except Exception as e:
        print_error(f"\n\nError inesperado: {e}")
        sys.exit(1)
