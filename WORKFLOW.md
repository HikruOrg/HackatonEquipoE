# 📋 AI Talent Matcher - Workflow y Funcionalidades

## 🎯 Descripción General

AI Talent Matcher es una plataforma que **rankea candidatos automáticamente** basándose en qué tan bien encajan con una job description, utilizando análisis con LLM (Large Language Models) y scoring híbrido.

---

## 🔄 Workflow Completo de la Aplicación

### 1️⃣ Preparación de Datos (Pre-requisito)

#### 📂 Opción A: Auto-Procesamiento en Startup (Recomendado)

El backend **procesa automáticamente** archivos al iniciar:

```
data/
├── resumes/raw/              ← Coloca archivos aquí
│   ├── candidato1.pdf
│   ├── candidato2.json
│   └── candidato3.txt
└── job_descriptions/raw/     ← Coloca archivos aquí
    ├── senior_dev.pdf
    ├── frontend_react.json
    └── backend_python.txt
```

**¿Qué hace el sistema?**
- ✅ **Detecta** automáticamente archivos nuevos en las carpetas `raw/`
- ✅ **Valida** formatos y tamaño
- ✅ **Extrae** texto (de PDF/TXT) o parsea JSON
- ✅ **Convierte** a formato estructurado JSON
- ✅ **Guarda** en la base de datos (`data/storage/`)
- ✅ **Trackea** archivos procesados (no re-procesa duplicados)

**Formatos soportados:**
- `.pdf` - CVs/JDs en PDF
- `.json` - Datos estructurados
- `.txt` - Texto plano

#### 📂 Opción B: Upload Manual (API/Frontend)

Subir archivos a través de:
- **Frontend**: Pestaña "File Upload"
- **API**: Endpoints `/api/upload/resumes` y `/api/upload/job-description`

---

### 2️⃣ Iniciar Análisis

#### A través del Frontend

1. **Ir a "New Analysis"** → **"File Upload"**
2. **Seleccionar archivos**:
   - Uno o más **resumes** (PDF/JSON/TXT)
   - Una **job description** (PDF/JSON/TXT)
3. **Click "Start Analysis"**

#### A través de la API

```bash
POST /api/process
{
  "resume_files": ["resume1.json", "resume2.pdf"],
  "jd_file": "senior_backend.json"
}
```

---

### 3️⃣ Procesamiento Automático

El sistema ejecuta **en segundo plano** (background task):

#### Paso 1: Procesar Job Description
```
JD (PDF/JSON/TXT) → Extracción de texto → Parsing → JSON estructurado
                                                    ↓
                                          Identifica:
                                          - Must-have requirements
                                          - Nice-to-have requirements
                                          - Años de experiencia
                                          - Skills técnicos
```

#### Paso 2: Procesar Resumes
```
Resume (PDF/JSON/TXT) → Extracción → Parsing → JSON estructurado
                                               ↓
                                     Identifica:
                                     - Experiencia laboral
                                     - Skills
                                     - Educación
                                     - Años de experiencia
```

#### Paso 3: Análisis con LLM (Google Gemini)
Para cada candidato:
```
LLM Analyzer recibe:
├── Resume (JSON estructurado)
└── Job Description (JSON estructurado)
      ↓
Analiza:
├── Similarity Score (0-100)
├── Must-Have Matches (cuáles cumple)
├── Nice-to-Have Matches
├── Fortalezas del candidato
├── Gaps identificados
└── Reason Codes (explicación)
```

#### Paso 4: Scoring Híbrido
```
Final Score = (Similarity × 60%) + (Must-Have × 30%) + (Recency × 10%)

Donde:
- Similarity Score: Match semántico del LLM (0-100)
- Must-Have Score: % de requisitos obligatorios cumplidos
- Recency Boost: Experiencia reciente relevante
```

#### Paso 5: Ranking y Explainability
```
Ordenar candidatos por Final Score (descendente)
    ↓
Para cada candidato:
├── Generar Reason Codes (por qué rankea en esta posición)
├── Mapear Hits (qué requisitos cumple)
└── Identificar secciones relevantes del resume
```

---

### 4️⃣ Ver Resultados

#### En el Frontend

**Opción A: Vista "Processing"**
- Monitoreo en tiempo real
- Progress bar
- Tiempo estimado

**Opción B: Vista "Results"**
- Tabla de candidatos rankeados
- Scores detallados por columna:
  - Overall Score (final)
  - Similarity Score
  - Must-Have Hits
  - Recency Boost
- Export a CSV

**Opción C: Vista "Job Descriptions & Results"**
- Grid de todas las JDs procesadas
- Click en JD → Ver detalles + candidatos rankeados
- Top 3 con badges 🥇🥈🥉
- Reason codes y matched requirements

#### A través de la API

```bash
# Ver estado del procesamiento
GET /api/process/status

# Obtener resultados completos
GET /api/results

# Ver detalles de un candidato
GET /api/results/{candidate_id}

# Exportar a CSV
GET /api/export/csv
```

---

## ✅ Funcionalidades Soportadas

### 📁 Gestión de Archivos

| Funcionalidad | Soportado | Formatos | Notas |
|--------------|-----------|----------|-------|
| Upload Resumes | ✅ | PDF, JSON, TXT | Múltiples archivos |
| Upload Job Descriptions | ✅ | PDF, JSON, TXT | Un archivo por análisis |
| Auto-procesamiento Startup | ✅ | PDF, JSON, TXT | Detecta archivos nuevos |
| Tracking de procesados | ✅ | Todos | Evita duplicados |
| Validación de archivos | ✅ | Todos | Tamaño, formato, contenido |

### 🤖 Análisis con LLM

| Funcionalidad | Soportado | Provider | Notas |
|--------------|-----------|----------|-------|
| Análisis semántico | ✅ | Google Gemini | gemini-2.5-flash |
| Similarity scoring | ✅ | LLM | 0-100 scale |
| Must-have matching | ✅ | LLM | Detecta cumplimiento |
| Reason codes | ✅ | LLM | Explica ranking |
| Fortalezas/Gaps | ✅ | LLM | Análisis cualitativo |
| Fallback sin LLM | ✅ | Rule-based | Si falla API |

### 📊 Scoring y Ranking

| Funcionalidad | Soportado | Configuración | Notas |
|--------------|-----------|---------------|-------|
| Scoring híbrido | ✅ | `.env` weights | 60% similarity + 30% must-have + 10% recency |
| Rule-based boosting | ✅ | Configurable | Skills match, experience, etc. |
| Recency scoring | ✅ | Automático | Experiencia reciente |
| Ranking automático | ✅ | Por final score | Descendente |

### 💾 Almacenamiento

| Funcionalidad | Soportado | Ubicación | Notas |
|--------------|-----------|-----------|-------|
| Storage local | ✅ | `data/storage/` | JSON files |
| Listar resumes | ✅ | API endpoint | Con metadatos |
| Listar JDs | ✅ | API endpoint | Con metadatos |
| Buscar archivos | ✅ | API endpoint | Por texto |
| Eliminar archivos | ✅ | API endpoint | Soft delete |
| Cache de respuestas | ✅ | `data/cache/` | LLM responses, embeddings |

### 📤 Exportación

| Funcionalidad | Soportado | Formato | Notas |
|--------------|-----------|---------|-------|
| Export CSV | ✅ | CSV | Resultados completos |
| Timestamps | ✅ | ISO 8601 | En nombre archivo |
| Codificación | ✅ | UTF-8 | Configurable |

### 🔍 Explainability

| Funcionalidad | Soportado | Descripción |
|--------------|-----------|-------------|
| Reason Codes | ✅ | Explica por qué rankea así |
| Hit Mapper | ✅ | Mapea requisitos cumplidos a secciones del resume |
| Must-Have Hits | ✅ | Lista de requisitos obligatorios cumplidos |
| Nice-to-Have Hits | ✅ | Lista de requisitos opcionales cumplidos |
| Fortalezas | ✅ | Puntos fuertes del candidato |
| Gaps | ✅ | Áreas de mejora o faltantes |

---

## ❌ Funcionalidades NO Soportadas

### Limitaciones Actuales

| Funcionalidad | Status | Razón |
|--------------|--------|-------|
| **Múltiples JDs simultáneas** | ❌ | Solo 1 JD por análisis |
| **Edición de resumes** | ❌ | Solo lectura |
| **Edición de JDs** | ❌ | Solo lectura |
| **Re-análisis automático** | ❌ | Debe iniciar manualmente |
| **Análisis incremental** | ❌ | Siempre procesa todos |
| **Storage en cloud** | ❌ | Solo local filesystem |
| **Autenticación/Usuarios** | ⚠️ | Mock (frontend only) |
| **Permisos/Roles** | ❌ | No implementado |
| **Base de datos SQL** | ❌ | Solo JSON files |
| **OCR avanzado** | ❌ | PDF texto solo (no imágenes) |
| **Procesamiento de imágenes** | ❌ | Solo texto |
| **Video resumes** | ❌ | No soportado |
| **Enlaces a LinkedIn/GitHub** | ❌ | No extrae automáticamente |
| **Scraping de perfiles** | ❌ | No implementado |
| **Integración con ATS** | ❌ | No disponible |
| **Email notifications** | ❌ | No implementado |
| **Webhooks** | ❌ | No disponible |
| **Batch processing programado** | ❌ | Solo manual o startup |
| **Versionado de JDs** | ❌ | No rastrea cambios |
| **Histórico de análisis** | ❌ | Solo último resultado |
| **Comparación entre candidatos** | ❌ | Solo ranking |
| **Entrevistas automáticas** | ❌ | No implementado |
| **Evaluaciones técnicas** | ❌ | No integrado |

### Limitaciones de Formato

| Tipo de Archivo | Limitación |
|-----------------|------------|
| **PDF** | Max 50MB, solo texto extraíble (no OCR) |
| **JSON** | Max 10MB, debe tener estructura válida |
| **TXT** | Max 10MB, UTF-8 o latin-1 only |
| **Word (.docx)** | ❌ No soportado |
| **Excel (.xlsx)** | ❌ No soportado |
| **Images (JPG/PNG)** | ❌ No soportado |

### Limitaciones de Procesamiento

| Aspecto | Limitación |
|---------|------------|
| **Concurrencia** | Procesa 1 análisis a la vez |
| **Timeout LLM** | 60 segundos por request |
| **Rate limiting** | Depende de API key de Gemini |
| **Resumes por análisis** | Sin límite técnico (pero 1 JD) |
| **Cache TTL** | 30 días (configurable) |

---

## 🔧 Configuración y Personalización

### Variables de Entorno (.env)

```env
# LLM Configuration
LLM_PROVIDER=gemini
GOOGLE_API_KEY=tu_api_key

# Scoring Weights (deben sumar 1.0)
SIMILARITY_WEIGHT=0.6      # Ajustar importancia de similarity
MUST_HAVE_BOOST_WEIGHT=0.3 # Ajustar importancia de must-have
RECENCY_BOOST_WEIGHT=0.1   # Ajustar importancia de recency

# LLM Parameters
LLM_TEMPERATURE=0.3        # Creatividad (0=determinístico, 1=creativo)
LLM_MAX_TOKENS=2000        # Longitud de respuesta
LLM_TIMEOUT=60             # Timeout en segundos

# Cache
ENABLE_CACHE=true
CACHE_TTL=2592000          # 30 días en segundos

# Paths
STORAGE_PATH=./data/storage
CACHE_PATH=./data/cache
OUTPUT_DIR=./data/output
```

---

## 📊 Estados del Sistema

### Estados de Procesamiento

```
IDLE → PROCESSING → COMPLETED
   ↓                    ↓
   └─────→ ERROR ←──────┘
```

| Estado | Descripción | Acciones Permitidas |
|--------|-------------|---------------------|
| `idle` | Sin procesamiento activo | Iniciar nuevo análisis |
| `processing` | Análisis en curso | Ver progreso, NO iniciar otro |
| `completed` | Análisis finalizado | Ver resultados, exportar, iniciar nuevo |
| `error` | Falló el procesamiento | Ver errores, reintentar |

---

## 🎯 Casos de Uso Típicos

### Caso 1: Recruitment Agency
```
1. Coloca 50 CVs en data/resumes/raw/
2. Coloca JD en data/job_descriptions/raw/
3. Inicia servidor → Auto-procesa archivos
4. API: POST /api/process con todos los resumes
5. Obtiene top 10 candidatos rankeados
6. Exporta resultados a CSV para cliente
```

### Caso 2: HR Interno
```
1. Upload resumes via frontend
2. Upload job description via frontend
3. Click "Start Analysis"
4. Monitorea progreso en tiempo real
5. Revisa candidatos en "Job Descriptions & Results"
6. Filtra por must-have requirements
```

### Caso 3: Desarrollo/Testing
```
1. Usa archivos de ejemplo en raw/
2. Ejecuta test_auto_processor.py
3. Verifica procesamiento correcto
4. Inicia servidor y prueba API endpoints
5. Valida resultados en frontend
```

---

## 🚨 Manejo de Errores

### Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `Processing already in progress` | Análisis ya corriendo | Esperar a que termine |
| `No module named 'pdfplumber'` | Dependencia faltante | `pip install -r requirements.txt` |
| `GOOGLE_API_KEY is required` | API key no configurada | Agregar en `.env` |
| `File too large` | Archivo > límite | Reducir tamaño o dividir |
| `Invalid JSON format` | JSON malformado | Validar estructura |
| `No text extracted from PDF` | PDF solo imágenes | Convertir a texto o usar OCR externo |
| `LLM timeout` | Request muy largo | Reducir tamaño de texto o aumentar timeout |

---

## 📈 Métricas y Monitoreo

### Logs Disponibles

El sistema registra:
- ✅ Archivos procesados/skipped/failed
- ✅ Tiempo de procesamiento por archivo
- ✅ Errores de validación
- ✅ Respuestas del LLM
- ✅ Scores calculados
- ✅ Warnings de configuración

### Formato de Logs

```
2025-11-06 17:30:45 - src.startup.auto_processor - INFO - Processing resume: maria_garcia.json
2025-11-06 17:30:46 - src.startup.auto_processor - INFO - ✓ Successfully processed resume: maria_garcia.json
```

---

## 🔐 Seguridad y Privacidad

### ⚠️ Consideraciones Importantes

| Aspecto | Estado Actual | Recomendación para Producción |
|---------|---------------|-------------------------------|
| **API Keys** | En `.env` local | Usar secrets manager |
| **CORS** | `allow_origins=["*"]` | Limitar a dominios específicos |
| **Autenticación** | Mock (frontend) | Implementar auth real (JWT, OAuth) |
| **Datos de candidatos** | Sin encriptación | Encriptar datos sensibles |
| **File uploads** | Sin escaneo | Agregar antivirus/malware scan |
| **Rate limiting** | No implementado | Agregar para producción |
| **HTTPS** | No forzado | Forzar HTTPS en producción |

---

## 📚 Recursos Adicionales

- **[README.md](readme.md)** - Guía de inicio rápido
- **[TXT_SUPPORT.md](TXT_SUPPORT.md)** - Soporte de archivos de texto
- **[SETUP.md](SETUP.md)** - Configuración detallada
- **[TEST_API_GUIDE.md](TEST_API_GUIDE.md)** - Testing de API
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)

---

**Última actualización**: 6 de noviembre de 2025  
**Versión**: 1.0.0
