#!/usr/bin/env python3
"""Test específico para verificar el procesamiento de Resume/CV en PDF."""
import requests
import time
from pathlib import Path
import sys

# Configuración
API_BASE_URL = "http://localhost:8000"
TEST_PDF_PATH = Path(__file__).parent.parent / "data" / "resumes" / "raw" / "genome_alejob600.pdf"
TEST_JD_PATH = Path(__file__).parent.parent / "data" / "job_descriptions" / "raw" / "test_job.json"

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

def print_info(message: str):
    """Imprime mensaje informativo."""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")

def check_server():
    """Verificar que el servidor está corriendo."""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        return response.status_code == 200
    except:
        return False

def test_upload_pdf_resume():
    """Test: Subir Resume en PDF."""
    print_section("Test 1: Subir Resume PDF")
    
    if not TEST_PDF_PATH.exists():
        print_error(f"PDF no encontrado: {TEST_PDF_PATH}")
        return None
    
    print_info(f"Archivo: {TEST_PDF_PATH.name}")
    print_info(f"Tamaño: {TEST_PDF_PATH.stat().st_size / 1024:.2f} KB")
    
    try:
        endpoint = "/api/upload/resumes"
        print_info(f"Endpoint: POST {endpoint}")
        with open(TEST_PDF_PATH, 'rb') as f:
            files = {'files': (TEST_PDF_PATH.name, f, 'application/pdf')}
            response = requests.post(
                f"{API_BASE_URL}{endpoint}",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"PDF subido: {data.get('uploaded', 0)} archivo(s)")
            if data.get('files'):
                for file_info in data['files']:
                    print_info(f"  - {file_info.get('filename')}")
                    print_info(f"    Type: {file_info.get('type')}")
                    print_info(f"    Path: {file_info.get('path')}")
            return data
        else:
            print_error(f"Error al subir: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_upload_job_description():
    """Test: Subir job description de prueba."""
    print_section("Test 2: Subir Job Description (JSON)")
    
    if not TEST_JD_PATH.exists():
        print_error(f"JD no encontrado: {TEST_JD_PATH}")
        return None
    
    try:
        endpoint = "/api/upload/job-description"
        print_info(f"Endpoint: POST {endpoint}")
        with open(TEST_JD_PATH, 'rb') as f:
            files = {'file': (TEST_JD_PATH.name, f, 'application/json')}
            response = requests.post(
                f"{API_BASE_URL}{endpoint}",
                files=files,
                timeout=10
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Job Description subido: {data.get('filename')}")
            print_info(f"  Type: {data.get('type')}")
            print_info(f"  Path: {data.get('path')}")
            return data
        else:
            print_error(f"Error al subir: {response.status_code}")
            return None
            
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def test_process_with_pdf(resume_files, jd_file):
    """Test: Procesar con PDF Resume."""
    print_section("Test 3: Procesar con PDF Resume")
    
    try:
        endpoint = "/api/process"
        print_info(f"Endpoint: POST {endpoint}")
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
            return True
        else:
            print_error(f"Error: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_monitor_processing(max_wait=180):
    """Test: Monitorear procesamiento."""
    print_section("Test 4: Monitorear Procesamiento")
    
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
                        print_error(f"Errores: {len(data['errors'])}")
                        for error in data['errors'][:3]:  # Mostrar solo los primeros 3
                            print_error(f"  - {error}")
                    
                    return data
                    
                elif status == "error":
                    print()
                    print_error("Error en el procesamiento")
                    for error in data.get('errors', []):
                        print_error(f"  - {error}")
                    return None
                    
        except Exception as e:
            print_error(f"Error: {e}")
            return None
    
    print()
    print_error(f"Timeout después de {max_wait} segundos")
    return None

def test_get_results():
    """Test: Obtener y mostrar resultados."""
    print_section("Test 5: Obtener Resultados del Matching")
    
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
                print(f"{'=' * 60}")
                print(f"📊 Rank #{result.get('rank')}: {result.get('name', 'N/A')}")
                print(f"{'=' * 60}")
                print(f"   🎯 Score Final: {result.get('final_score', 0):.2f}")
                print(f"   📈 Score Similaridad: {result.get('similarity_score', 0):.2f}")
                print(f"   ✓  Must-Have Matches: {len(result.get('must_have_matches', []))}")
                
                if result.get('must_have_matches'):
                    print(f"      Requisitos cumplidos:")
                    for match in result.get('must_have_matches', [])[:5]:
                        print(f"         • {match}")
                
                print(f"   ⬆️  Recency Boost: {result.get('recency_boost', 0):.2f}")
                
                reason_codes = result.get('reason_codes', [])
                if reason_codes:
                    print(f"   💡 Reason Codes ({len(reason_codes)}):")
                    for code in reason_codes[:5]:
                        print(f"         • {code}")
                
                # Mostrar hit mappings si existen
                hit_mappings = result.get('hit_mappings', [])
                if hit_mappings:
                    print(f"   🎯 Hit Mappings ({len(hit_mappings)}):")
                    for mapping in hit_mappings[:3]:
                        print(f"         • {mapping.get('jd_requirement', 'N/A')}")
                        print(f"           → {mapping.get('resume_match', 'N/A')[:60]}...")
            
            return data
        else:
            print_error(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def main():
    """Ejecutar test completo con PDF."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'*' * 70}")
    print(f"🧪 TEST: Resume/CV PDF - {TEST_PDF_PATH.name}")
    print(f"{'*' * 70}{Colors.RESET}\n")
    
    # Verificar servidor
    print_info("Verificando servidor...")
    if not check_server():
        print_error("Servidor no disponible en http://localhost:8000")
        print_info("Inicia el servidor: python run_server.py")
        sys.exit(1)
    print_success("Servidor activo\n")
    
    # Test 1: Upload PDF Resume
    resume_response = test_upload_pdf_resume()
    if not resume_response or not resume_response.get('files'):
        print_error("\n⛔ No se pudo subir el PDF Resume")
        sys.exit(1)
    
    resume_files = [f['path'] for f in resume_response.get('files', [])]
    
    # Test 2: Upload Job Description
    jd_response = test_upload_job_description()
    if not jd_response or not jd_response.get('path'):
        print_error("\n⛔ No se pudo subir el Job Description")
        sys.exit(1)
    
    jd_file = jd_response.get('path')
    
    # Test 3: Start Processing
    if not test_process_with_pdf(resume_files, jd_file):
        print_error("\n⛔ No se pudo iniciar el procesamiento")
        sys.exit(1)
    
    # Test 4: Monitor Processing
    processing_result = test_monitor_processing(max_wait=180)
    if not processing_result:
        print_error("\n⛔ Procesamiento no completado")
        sys.exit(1)
    
    # Test 5: Get Results
    results = test_get_results()
    if not results:
        print_error("\n⛔ No se pudieron obtener resultados")
        sys.exit(1)
    
    # Resumen final
    print_section("✅ RESUMEN DEL TEST")
    print_success(f"PDF Resume/CV procesado correctamente: {TEST_PDF_PATH.name}")
    print_success(f"Candidatos evaluados: {len(results.get('results', []))}")
    print_info("El backend procesa correctamente PDFs de Resumes/CVs")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Test interrumpido{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Error inesperado: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
