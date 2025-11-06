# 🧪 Tests del Backend - AI Talent Matcher

Esta carpeta contiene todos los tests automatizados para verificar el correcto funcionamiento del backend.

## 📋 Tests Disponibles

### 1. `verify_setup.py` - Verificación de Configuración
**Propósito:** Verifica que el entorno esté correctamente configurado

**Ejecutar:**
```bash
python tests/verify_setup.py
```

**Verifica:**
- ✅ Versión de Python (3.9+)
- ✅ Dependencias instaladas
- ✅ Archivo `.env` existe
- ✅ API Keys configuradas
- ✅ Estructura de directorios
- ✅ Módulo de configuración

---

### 2. `test_llm_quick.py` - Test Rápido LLM (10 seg)
**Propósito:** Verificación rápida de conectividad con el LLM

**Ejecutar:**
```bash
python tests/test_llm_quick.py
```

**Prueba:**
- ✅ Inicialización del cliente LLM
- ✅ Respuesta simple del LLM

---

### 3. `test_llm_connection.py` - Test Completo LLM
**Propósito:** Test exhaustivo de la integración con LLM

**Ejecutar:**
```bash
python tests/test_llm_connection.py
```

**Prueba:**
- ✅ Respuesta de texto simple
- ✅ Respuesta JSON estructurada
- ✅ Análisis de matching simplificado
- ✅ Tiempos de respuesta

---

### 4. `test_api.py` - Suite Completa de Tests API
**Propósito:** Test end-to-end del API con archivos JSON

**Ejecutar:**
```bash
python tests/test_api.py
```

**Requiere:** Servidor corriendo en `http://localhost:8000`

**Prueba:**
- ✅ Health check
- ✅ Documentación API
- ✅ Upload de resumes (JSON)
- ✅ Upload de job descriptions (JSON)
- ✅ Procesamiento completo
- ✅ Monitoreo de estado
- ✅ Obtención de resultados
- ✅ Endpoints de storage
- ✅ Exportación a CSV

---

### 5. `test_api_pdf_resume.py` - Test con PDF Resume/CV
**Propósito:** Verificar procesamiento de Resumes/CVs en formato PDF

**Ejecutar:**
```bash
python tests/test_api_pdf_resume.py
```

**Requiere:** 
- Servidor corriendo
- Archivo `data/resumes/raw/genome_alejob600.pdf`

**Prueba:**
- ✅ Upload de PDF Resume
- ✅ Validación de PDF
- ✅ Extracción de texto del CV
- ✅ Procesamiento con PDF Resume
- ✅ Matching completo con JD
- ✅ Generación de resultados detallados

---

### 6. `test_api_runner.py` - Runner Automático
**Propósito:** Ejecuta `test_api.py` con verificación previa del servidor

**Ejecutar:**
```bash
python tests/test_api_runner.py
```

**Ventajas:**
- ✅ Verifica que el servidor esté activo antes de ejecutar
- ✅ Muestra instrucciones si el servidor no está corriendo
- ✅ Ejecuta la suite completa automáticamente

---

### 7. `run_api_tests.ps1` - Script PowerShell (Windows)
**Propósito:** Automatización completa para Windows

**Ejecutar:**
```powershell
.\tests\run_api_tests.ps1
```

**Hace:**
- ✅ Verifica/inicia el servidor automáticamente
- ✅ Espera a que el servidor esté listo
- ✅ Ejecuta todos los tests
- ✅ Pregunta si detener el servidor al finalizar

---

## 🚀 Guía de Uso Rápida

### Primer Uso

1. **Verificar configuración:**
   ```bash
   python tests/verify_setup.py
   ```

2. **Test rápido LLM:**
   ```bash
   python tests/test_llm_quick.py
   ```

3. **Iniciar servidor (nueva terminal):**
   ```bash
   python run_server.py
   ```

4. **Ejecutar tests API:**
   ```bash
   python tests/test_api_runner.py
   ```

### Tests Específicos

**Solo verificar LLM:**
```bash
python tests/test_llm_connection.py
```

**Solo probar PDF Resume:**
```bash
python tests/test_api_pdf_resume.py
```

**Suite completa:**
```bash
python tests/test_api.py
```

---

## 📊 Archivos de Prueba

Los tests usan estos archivos de ejemplo:

- **Resume:** `data/resumes/raw/test_resume.json`
  - Candidata: María García López
  - 5 años Python, FastAPI, Django

- **Job Description (JSON):** `data/job_descriptions/raw/test_job.json`
  - Posición: Senior Backend Developer
  - Requisitos: Python, FastAPI, PostgreSQL

- **Job Description (PDF):** `data/job_descriptions/raw/genome_alejob600.pdf`
  - PDF real para pruebas de extracción

---

## 🔧 Troubleshooting

### Error: "Module not found"
```bash
# Asegúrate de estar en el directorio raíz
cd D:\repos\HackatonEquipoE

# O activa el entorno virtual
.\venv\Scripts\Activate.ps1
```

### Error: "Server not available"
```bash
# Inicia el servidor en otra terminal
python run_server.py
```

### Error: "API key not configured"
```bash
# Edita el archivo .env y agrega tu API key
# Luego reinicia el servidor
```

### Error: "File not found"
```bash
# Los tests buscan archivos desde la raíz del proyecto
# Asegúrate de ejecutar desde: D:\repos\HackatonEquipoE
python tests/test_api.py
```

---

## 📈 Resultados Esperados

### ✅ Test Exitoso - `verify_setup.py`
```
✅ Python 3.12.10
✅ fastapi
✅ uvicorn
...
✅ ¡Todo listo!
```

### ✅ Test Exitoso - `test_llm_quick.py`
```
🚀 Test Rápido LLM...
   Provider: gemini
   ✅ Cliente inicializado
   ✅ Respuesta: OK
✅ ¡LLM FUNCIONA!
```

### ✅ Test Exitoso - `test_api.py`
```
Test 1: Health Check ✅
Test 2: API Docs ✅
Test 3: Upload Resume ✅
...
Test 9: Export CSV ✅
✅ Todos los tests completados
```

### ✅ Test Exitoso - `test_api_pdf_jd.py`
```
Test 1: Subir Job Description PDF ✅
Test 2: Subir Resume ✅
...
Test 5: Obtener Resultados ✅
✅ PDF JD procesado correctamente
```

---

## 🎯 Cobertura de Tests

| Componente | Test | Estado |
|------------|------|--------|
| Configuración | verify_setup.py | ✅ |
| LLM Client | test_llm_quick.py | ✅ |
| LLM Integration | test_llm_connection.py | ✅ |
| API Endpoints | test_api.py | ✅ |
| PDF Processing | test_api_pdf_jd.py | ✅ |
| JSON Processing | test_api.py | ✅ |
| Storage | test_api.py | ✅ |
| Export CSV | test_api.py | ✅ |
| Background Tasks | test_api.py | ✅ |

---

## 💡 Tips

1. **Ejecuta `verify_setup.py` primero** - Te ahorra tiempo si falta algo
2. **Usa `test_api_runner.py`** - Verifica el servidor automáticamente
3. **Revisa los logs del servidor** - Útil para debugging
4. **Los tests son independientes** - Puedes ejecutarlos en cualquier orden
5. **El servidor debe estar corriendo** - Excepto para verify_setup y tests LLM

---

## 📞 Más Información

- **Guía completa de tests:** `TEST_API_GUIDE.md` (raíz del proyecto)
- **Formatos de entrada:** `JOB_DESCRIPTION_FORMATS.md`, `RESUME_FORMATS.md`
- **Setup general:** `SETUP.md`, `QUICKSTART.md`
- **Reporte de tests:** `BACKEND_TEST_REPORT.md`

---

**Última actualización:** 2025-11-06
**Estado:** ✅ Todos los tests funcionando
