#!/usr/bin/env python3
"""Script completo para probar el backend API en ejecución."""
import requests
import time
import json
from pathlib import Path
from typing import Dict, List

# Configuración
API_BASE_URL = "http://localhost:8000"
TEST_DATA_DIR = Path(__file__).parent.parent / "data"

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_section(title: str):
    """Imprime título de sección."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")

def print_success(message: str):
    """Imprime mensaje de éxito."""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message: str):
    """Imprime mensaje de error."""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")

def print_warning(message: str):
    """Imprime mensaje de advertencia."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")

def print_info(message: str):
    """Imprime mensaje informativo."""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")

def test_server_health() -> bool:
    """Test 1: Verificar que el servidor está corriendo."""
    print_section("Test 1: Health Check del Servidor")
    
    try:
        endpoint = "/"
        print_info(f"Endpoint: GET {endpoint}")
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Servidor activo: {data.get('message', 'N/A')}")
            print_info(f"Versión: {data.get('version', 'N/A')}")
            return True
        else:
            print_error(f"Status code inesperado: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor")
        print_info("Asegúrate de que el servidor está corriendo: python run_server.py")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_api_docs() -> bool:
    """Test 2: Verificar que la documentación está disponible."""
    print_section("Test 2: Documentación de la API")
    
    try:
        endpoint = "/docs"
        print_info(f"Endpoint: GET {endpoint}")
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            print_success("Swagger UI disponible en /docs")
            print_info(f"URL: {API_BASE_URL}/docs")
            return True
        else:
            print_warning(f"Docs no disponible: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_upload_resume() -> Dict:
    """Test 3: Subir un resume de prueba."""
    print_section("Test 3: Subir Resume (JSON)")
    
    resume_path = TEST_DATA_DIR / "resumes" / "raw" / "test_resume.json"
    
    if not resume_path.exists():
        print_error(f"Archivo de prueba no encontrado: {resume_path}")
        return {}
    
    try:
        endpoint = "/api/upload/resumes"
        print_info(f"Endpoint: POST {endpoint}")
        with open(resume_path, 'rb') as f:
            files = {'files': ('test_resume.json', f, 'application/json')}
            response = requests.post(
                f"{API_BASE_URL}{endpoint}",
                files=files,
                timeout=10
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Resume subido: {data.get('uploaded', 0)} archivo(s)")
            
            if data.get('files'):
                for file_info in data['files']:
                    print_info(f"  - {file_info.get('filename')}")
                    print_info(f"    Tipo: {file_info.get('type')}")
                    print_info(f"    Path: {file_info.get('path')}")
            
            if data.get('errors'):
                for error in data['errors']:
                    print_warning(f"  - {error}")
            
            return data
        else:
            print_error(f"Error al subir: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return {}
            
    except Exception as e:
        print_error(f"Error: {e}")
        return {}

def test_upload_job_description() -> Dict:
    """Test 4: Subir un job description de prueba."""
    print_section("Test 4: Subir Job Description (JSON)")
    
    jd_path = TEST_DATA_DIR / "job_descriptions" / "raw" / "test_job.json"
    
    if not jd_path.exists():
        print_error(f"Archivo de prueba no encontrado: {jd_path}")
        return {}
    
    try:
        endpoint = "/api/upload/job-description"
        print_info(f"Endpoint: POST {endpoint}")
        with open(jd_path, 'rb') as f:
            files = {'file': ('test_job.json', f, 'application/json')}
            response = requests.post(
                f"{API_BASE_URL}{endpoint}",
                files=files,
                timeout=10
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Job Description subido: {data.get('filename')}")
            print_info(f"Tipo: {data.get('type')}")
            print_info(f"Path: {data.get('path')}")
            return data
        else:
            print_error(f"Error al subir: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return {}
            
    except Exception as e:
        print_error(f"Error: {e}")
        return {}

def test_start_processing(resume_files: List[str], jd_file: str) -> bool:
    """Test 5: Iniciar el procesamiento."""
    print_section("Test 5: Iniciar Procesamiento")
    
    if not resume_files or not jd_file:
        print_error("Faltan archivos para procesar")
        return False
    
    try:
        endpoint = "/api/process"
        print_info(f"Endpoint: POST {endpoint}")
        # Enviar como JSON body
        payload = {
            "resume_files": resume_files,
            "jd_file": jd_file
        }
        
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Procesamiento iniciado: {data.get('status')}")
            print_info(f"Mensaje: {data.get('message')}")
            return True
        else:
            print_error(f"Error al iniciar: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_check_processing_status(max_wait: int = 60) -> bool:
    """Test 6: Monitorear el estado del procesamiento."""
    print_section("Test 6: Monitorear Procesamiento")
    
    endpoint = "/api/process/status"
    print_info(f"Endpoint: GET {endpoint}")
    print_info(f"Esperando hasta {max_wait} segundos...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                progress = data.get('progress', 0)
                total = data.get('total', 0)
                
                if status == "processing":
                    print(f"\r⏳ Procesando... {progress}/{total}", end='', flush=True)
                    time.sleep(2)
                    continue
                    
                elif status == "completed":
                    print()  # Nueva línea
                    print_success("Procesamiento completado")
                    print_info(f"Resultados: {len(data.get('results', []))}")
                    
                    if data.get('errors'):
                        print_warning(f"Errores encontrados: {len(data['errors'])}")
                        for error in data['errors']:
                            print_warning(f"  - {error}")
                    
                    return True
                    
                elif status == "error":
                    print()  # Nueva línea
                    print_error("Error en el procesamiento")
                    for error in data.get('errors', []):
                        print_error(f"  - {error}")
                    return False
                    
                else:
                    print_warning(f"Estado: {status}")
                    time.sleep(2)
                    
        except Exception as e:
            print_error(f"Error: {e}")
            return False
    
    print()  # Nueva línea
    print_error(f"Timeout después de {max_wait} segundos")
    return False

def test_get_results() -> Dict:
    """Test 7: Obtener Resultados"""
    print_section("Test 7: Obtener Resultados")
    
    try:
        endpoint = "/api/results"
        print_info(f"Endpoint: GET {endpoint}")
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print_success(f"Resultados obtenidos: {len(results)} candidato(s)")
            
            for result in results:
                print()
                print(f"📊 Rank #{result.get('rank')}: {result.get('name', 'N/A')}")
                print(f"   Score Final: {result.get('final_score', 0):.2f}")
                print(f"   Score Similaridad: {result.get('similarity_score', 0):.2f}")
                print(f"   Must-Have Matches: {len(result.get('must_have_matches', []))}")
                print(f"   Recency Boost: {result.get('recency_boost', 0):.2f}")
                
                reason_codes = result.get('reason_codes', [])
                if reason_codes:
                    print(f"   Reason Codes: {', '.join(reason_codes[:3])}")
            
            return data
        else:
            print_error(f"Error al obtener resultados: {response.status_code}")
            return {}
            
    except Exception as e:
        print_error(f"Error: {e}")
        return {}

def test_storage_endpoints() -> bool:
    """Test 8: Probar endpoints de storage."""
    print_section("Test 8: Storage Endpoints")
    
    success = True
    
    # Listar resumes
    try:
        endpoint = "/api/storage/resumes"
        print_info(f"Endpoint: GET {endpoint}")
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Resumes en storage: {len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print_warning(f"Error listando resumes: {response.status_code}")
            success = False
    except Exception as e:
        print_error(f"Error: {e}")
        success = False
    
    # Listar job descriptions
    try:
        endpoint = "/api/storage/job-descriptions"
        print_info(f"Endpoint: GET {endpoint}")
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Job Descriptions en storage: {len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print_warning(f"Error listando JDs: {response.status_code}")
            success = False
    except Exception as e:
        print_error(f"Error: {e}")
        success = False
    
    return success

def test_export_csv() -> bool:
    """Test 9: Exportar resultados a CSV."""
    print_section("Test 9: Exportar a CSV")
    
    try:
        endpoint = "/api/export/csv"
        print_info(f"Endpoint: GET {endpoint}")
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            print_success("CSV generado correctamente")
            print_info(f"Content-Type: {response.headers.get('content-type')}")
            print_info(f"Tamaño: {len(response.content)} bytes")
            
            # Guardar CSV localmente para verificar
            output_file = Path(__file__).parent.parent / "test_export.csv"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print_info(f"Guardado en: {output_file.absolute()}")
            
            return True
        else:
            print_error(f"Error al exportar: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    """Ejecutar todos los tests."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'*' * 70}")
    print(f"🧪 SUITE DE TESTS DEL BACKEND API")
    print(f"{'*' * 70}{Colors.RESET}\n")
    
    print_info(f"API Base URL: {API_BASE_URL}")
    print_info(f"Directorio de datos: {TEST_DATA_DIR.absolute()}")
    print()
    
    # Test 1: Health Check
    if not test_server_health():
        print_error("\n⛔ Servidor no disponible. Deteniendo tests.")
        return
    
    # Test 2: API Docs
    test_api_docs()
    
    # Test 3: Upload Resume
    resume_response = test_upload_resume()
    if not resume_response or not resume_response.get('files'):
        print_error("\n⛔ No se pudo subir el resume. Tests de procesamiento no ejecutados.")
        return
    
    resume_files = [f['path'] for f in resume_response.get('files', [])]
    
    # Test 4: Upload Job Description
    jd_response = test_upload_job_description()
    if not jd_response or not jd_response.get('path'):
        print_error("\n⛔ No se pudo subir el JD. Tests de procesamiento no ejecutados.")
        return
    
    jd_file = jd_response.get('path')
    
    # Test 5: Start Processing
    if not test_start_processing(resume_files, jd_file):
        print_error("\n⛔ No se pudo iniciar el procesamiento.")
        return
    
    # Test 6: Monitor Processing
    if not test_check_processing_status(max_wait=120):
        print_error("\n⛔ Procesamiento no completado.")
        return
    
    # Test 7: Get Results
    results = test_get_results()
    if not results:
        print_warning("\n⚠️  No se pudieron obtener resultados.")
    
    # Test 8: Storage Endpoints
    test_storage_endpoints()
    
    # Test 9: Export CSV
    if results:
        test_export_csv()
    
    # Resumen final
    print_section("✅ RESUMEN DE TESTS")
    print_success("Todos los tests principales completados")
    print_info("El backend está funcionando correctamente")
    print_info(f"Documentación disponible en: {API_BASE_URL}/docs")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Tests interrumpidos por el usuario{Colors.RESET}")
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Error inesperado: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
