# 🧪 Guía de Tests del Backend API

## 📋 Scripts de Testing Disponibles

### 1. `test_api.py` - Suite Completa de Tests
Script principal que prueba todos los endpoints del API:
- ✅ Health check del servidor
- ✅ Documentación API
- ✅ Upload de resumes
- ✅ Upload de job descriptions  
- ✅ Procesamiento de matching
- ✅ Obtención de resultados
- ✅ Endpoints de storage
- ✅ Exportación a CSV

### 2. `test_api_runner.py` - Verificador y Runner
Verifica que el servidor esté corriendo antes de ejecutar tests.

### 3. `run_api_tests.ps1` - Script PowerShell Automatizado
Inicia el servidor automáticamente y ejecuta los tests (solo Windows).

## 🚀 Cómo Ejecutar los Tests

### Opción 1: Manual (Recomendado)

**Paso 1:** Abre una terminal y inicia el servidor
```powershell
.\venv\Scripts\Activate.ps1
python run_server.py
```

**Paso 2:** Abre OTRA terminal y ejecuta los tests
```powershell
.\venv\Scripts\Activate.ps1
python test_api.py
```

### Opción 2: Con el Runner

```powershell
.\venv\Scripts\Activate.ps1
python test_api_runner.py
```

Si el servidor no está corriendo, te dirá cómo iniciarlo.

### Opción 3: Automático con PowerShell (Windows)

```powershell
.\run_api_tests.ps1
```

Esto:
1. Inicia el servidor automáticamente
2. Espera a que esté listo
3. Ejecuta todos los tests
4. Te pregunta si quieres detener el servidor

## 📊 Qué Hace Cada Test

### Test 1: Health Check
```
✅ Verifica que el servidor responde en http://localhost:8000
```

### Test 2: API Documentation
```
✅ Verifica que Swagger UI está disponible en /docs
```

### Test 3: Upload Resume
```
✅ Sube el archivo: data/resumes/raw/test_resume.json
✅ Verifica que el archivo se procesa correctamente
```

### Test 4: Upload Job Description
```
✅ Sube el archivo: data/job_descriptions/raw/test_job.json
✅ Verifica que el archivo se procesa correctamente
```

### Test 5: Start Processing
```
✅ Inicia el procesamiento de matching
✅ Envía los archivos al sistema de análisis
```

### Test 6: Monitor Processing
```
✅ Monitorea el progreso del procesamiento
✅ Espera hasta 120 segundos
✅ Muestra progreso en tiempo real
```

### Test 7: Get Results
```
✅ Obtiene los resultados del matching
✅ Muestra scores y ranking
✅ Muestra reason codes
```

### Test 8: Storage Endpoints
```
✅ Lista resumes almacenados
✅ Lista job descriptions almacenados
```

### Test 9: Export CSV
```
✅ Exporta resultados a CSV
✅ Guarda el archivo como test_export.csv
```

## 📁 Archivos de Prueba

Los tests usan estos archivos de ejemplo (ya creados):

- **Resume de prueba**: `data/resumes/raw/test_resume.json`
  - Candidata: María García López
  - 5 años experiencia Python
  - Conocimiento FastAPI, Django, PostgreSQL

- **Job Description de prueba**: `data/job_descriptions/raw/test_job.json`
  - Posición: Senior Backend Developer
  - Requisitos: Python, FastAPI, PostgreSQL, Docker

## 🎯 Resultado Esperado

Si todo funciona correctamente, verás:

```
======================================================================
🧪 SUITE DE TESTS DEL BACKEND API
======================================================================

Test 1: Health Check del Servidor
✅ Servidor activo: AI Talent Matcher API
ℹ️  Versión: 1.0.0

Test 2: Documentación de la API
✅ Swagger UI disponible en /docs

Test 3: Subir Resume (JSON)
✅ Resume subido: 1 archivo(s)

Test 4: Subir Job Description (JSON)
✅ Job Description subido: test_job.json

Test 5: Iniciar Procesamiento
✅ Procesamiento iniciado: started

Test 6: Monitorear Procesamiento
⏳ Procesando... 1/1
✅ Procesamiento completado

Test 7: Obtener Resultados
✅ Resultados obtenidos: 1 candidato(s)
📊 Rank #1: María García López
   Score Final: 0.95
   Score Similaridad: 0.90
   Must-Have Matches: 5

Test 8: Storage Endpoints
✅ Resumes en storage: 1
✅ Job Descriptions en storage: 1

Test 9: Exportar a CSV
✅ CSV generado correctamente
ℹ️  Guardado en: test_export.csv

✅ RESUMEN DE TESTS
✅ Todos los tests principales completados
```

## 🔧 Troubleshooting

### Error: "No se puede conectar al servidor"
```
❌ El servidor no está corriendo
```
**Solución**: Inicia el servidor en otra terminal con `python run_server.py`

### Error: "Archivo de prueba no encontrado"
```
❌ Archivo de prueba no encontrado: data/resumes/raw/test_resume.json
```
**Solución**: Los archivos ya deberían existir. Verifica la estructura de carpetas.

### Error: Timeout en procesamiento
```
❌ Timeout después de 120 segundos
```
**Solución**: 
- El LLM puede estar lento
- Verifica tu API key y conexión a internet
- Revisa los logs del servidor

### Error: "Processing not completed"
```
❌ Processing not completed
```
**Solución**: El procesamiento falló. Revisa:
- Los logs del servidor
- Que tu API key sea válida
- Que el LLM esté respondiendo (ejecuta `python test_llm_quick.py`)

## 📝 Tests Adicionales

### Probar solo la conexión LLM:
```powershell
python test_llm_quick.py
```

### Probar conexión LLM completa:
```powershell
python test_llm_connection.py
```

### Verificar configuración general:
```powershell
python verify_setup.py
```

## 🌐 Endpoints de la API

Una vez que el servidor esté corriendo, puedes probar manualmente:

```powershell
# Health check
curl http://localhost:8000/

# Ver documentación interactiva
# Abre en navegador: http://localhost:8000/docs

# Ver documentación alternativa
# Abre en navegador: http://localhost:8000/redoc
```

## 💡 Consejos

1. **Dos terminales**: Es más fácil tener el servidor en una terminal y ejecutar tests en otra
2. **Logs del servidor**: Revisa los logs para ver qué está pasando internamente
3. **Swagger UI**: Usa http://localhost:8000/docs para probar endpoints manualmente
4. **Archivos de prueba**: Puedes crear tus propios archivos JSON de prueba

## 📞 Siguiente Paso

Después de que los tests pasen:
1. El backend está 100% funcional
2. Puedes integrar con el frontend
3. Puedes probar con tus propios CVs y job descriptions
4. La API está lista para producción (con las configuraciones adecuadas)
