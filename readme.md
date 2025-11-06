# 🎯 AI Talent Matcher

Sistema inteligente de matching entre candidatos y posiciones laborales utilizando LLMs (Large Language Models) y scoring híbrido.

## 📖 Descripción del Proyecto

AI Talent Matcher es una plataforma completa que analiza resumes/CVs y job descriptions para generar rankings de candidatos basados en:

- **Análisis Semántico con LLM** (Google Gemini): Evaluación profunda de experiencia, skills y fit cultural
- **Scoring Híbrido**: Combina similarity score, must-have requirements, y recency boost
- **Explainability**: Reason codes detallados que explican por qué cada candidato es rankeado
- **Procesamiento de Múltiples Formatos**: Soporta archivos PDF, JSON y TXT
- **API REST**: Backend robusto con FastAPI
- **UI Moderna**: Frontend React con Material-UI

## 🏗️ Arquitectura

```
┌─────────────────┐
│  Frontend       │
│  React + MUI    │
│  Port: 3000     │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  Backend        │
│  FastAPI        │
│  Port: 8000     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌────────┐ ┌──────┐  ┌────────┐
│ LLM    │ │ PDF  │  │ Local  │
│ Gemini │ │ Proc │  │ Storage│
└────────┘ └──────┘  └────────┘
```

## 🛠️ Stack Tecnológico

### Backend
- **Python**: 3.12
- **Framework**: FastAPI
- **LLM**: Google Gemini (gemini-2.5-flash) via LangChain
- **PDF Processing**: pdfplumber
- **Data**: Pandas, JSON
- **Scoring**: Custom hybrid scorer (similarity + rule-based)

### Frontend
- **Framework**: React 18 + TypeScript
- **UI Library**: Material-UI (MUI) v6
- **Build Tool**: Vite
- **State Management**: TanStack Query (React Query)
- **HTTP Client**: Ky
- **Styling**: Emotion + Tailwind CSS

### Storage
- **Local File System**: JSON files para resumes y job descriptions
- **Cache**: LLM responses y embeddings (opcional)
- **Export**: CSV para resultados

## 🚀 Guía de Inicio Rápido

### Requisitos Previos

- **Python**: 3.12 o superior
- **Node.js**: 18.x o superior
- **Google Gemini API Key**: [Obtener aquí](https://makersuite.google.com/app/apikey)

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd HackatonEquipoE
```

### 2. Configurar Backend

#### 2.1 Crear Entorno Virtual

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate
```

#### 2.2 Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### 2.3 Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# LLM Configuration
LLM_PROVIDER=gemini
GOOGLE_API_KEY=tu_api_key_aqui

# Model Settings
LLM_MODEL=gemini-2.5-flash
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=2000
LLM_TIMEOUT=60

# Scoring Weights
SCORE_WEIGHT_SIMILARITY=0.6
SCORE_WEIGHT_MUST_HAVE=0.3
SCORE_WEIGHT_RECENCY=0.1

# Processing
MAX_WORKERS=4
BATCH_SIZE=10

# Cache
ENABLE_CACHE=true
CACHE_TTL=3600

# PDF Settings
MAX_PDF_SIZE_MB=50
```

**📝 Nota**: Usa el archivo `.env.example` como plantilla.

#### 2.4 Verificar Configuración

```bash
python tests/verify_setup.py
```

Deberías ver:
```
✅ Python 3.12.x
✅ Todas las dependencias instaladas
✅ Archivo .env encontrado
✅ GOOGLE_API_KEY configurada
✅ Directorios creados
```

#### 2.5 Iniciar Backend

```bash
python run_server.py
```

El backend estará disponible en: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### 3. Configurar Frontend

#### 3.1 Instalar Dependencias

```bash
cd FrontEnd
npm install
```

#### 3.2 Configurar Variables de Entorno

El archivo `.env.local` ya está configurado:

```env
VITE_API_BASE_URL=http://localhost:8000
```

#### 3.3 Iniciar Frontend

```bash
npm run dev
```

El frontend se abrirá automáticamente en: `http://localhost:3000`

## 📂 Estructura del Proyecto

```
HackatonEquipoE/
├── src/                          # Backend Source Code
│   ├── main.py                   # FastAPI app
│   ├── config.py                 # Configuration
│   ├── llm/                      # LLM integration (Gemini)
│   │   ├── client.py            # LLM client
│   │   └── analyzer.py          # Analysis logic
│   ├── pdf_processing/          # PDF extraction
│   ├── preprocessing/           # Resume & JD parsing
│   ├── scoring/                 # Hybrid scorer
│   ├── storage/                 # File storage
│   ├── export/                  # CSV export
│   ├── prompts/                 # LLM prompts
│   └── explainability/          # Reason codes
├── tests/                        # Test suite
│   ├── verify_setup.py          # Configuration check
│   ├── test_llm_quick.py        # LLM quick test
│   ├── test_llm_connection.py   # LLM full test
│   ├── test_api.py              # API endpoints test
│   └── test_api_pdf_resume.py   # PDF processing test
├── data/                         # Data storage
│   ├── resumes/                 # Uploaded resumes
│   │   ├── raw/                 # Original files
│   │   └── processed/           # Parsed data
│   ├── job_descriptions/        # Uploaded JDs
│   │   ├── raw/
│   │   └── processed/
│   ├── storage/                 # Persistent storage
│   ├── cache/                   # LLM cache
│   └── output/                  # Generated files (CSV)
├── FrontEnd/                     # Frontend Application
│   ├── src/
│   │   └── app/
│   │       └── (control-panel)/
│   │           └── apps/
│   │               └── talent-matcher/
│   │                   ├── api/              # API services
│   │                   ├── components/       # React components
│   │                   │   └── views/
│   │                   │       ├── TalentMatcherAppView.tsx
│   │                   │       ├── FileUploadView.tsx
│   │                   │       ├── JobDescriptionsView.tsx
│   │                   │       ├── ProcessingView.tsx
│   │                   │       └── ResultsView.tsx
│   │                   └── route.tsx
│   ├── vite.config.mts          # Vite config (proxy)
│   └── package.json
├── .env                          # Environment variables (crear)
├── .env.example                  # Template
├── requirements.txt              # Python dependencies
├── run_server.py                 # Start backend
└── run_all_tests.py              # Run all tests
```

## 🎯 Uso de la Aplicación

### Flujo Completo

#### 1. Nueva Análisis

**Opción A: File Upload (Recomendado)**

1. Ir a `http://localhost:3000`
2. Seleccionar pestaña **"New Analysis"** → **"File Upload"**
3. Subir uno o más resumes (PDF, JSON, o TXT)
4. Subir una job description (PDF, JSON, o TXT)
5. Click en **"Start Analysis"**
6. Monitorear progreso en tiempo real
7. Ver resultados rankeados

**Opción B: Manual Entry**

1. Pestaña **"New Analysis"** → **"Manual Entry"**
2. Completar formulario de Resume
3. Completar formulario de Job Description
4. Click en **"Submit & Analyze"**

#### 2. Ver Job Descriptions y Candidatos

1. Pestaña **"Job Descriptions & Results"**
2. Ver todas las JDs disponibles en formato grid
3. Click en una JD para ver:
   - Detalles de la posición
   - Requirements (Must-Have / Nice-to-Have)
   - **Candidatos rankeados** con:
     - Overall Score
     - Similarity Score
     - Must-Have Hits
     - Recency Boost
     - Reason Codes
     - Matched Requirements

### Formatos de Archivo

**Resume JSON:**
```json
{
  "candidate_id": "CAND001",
  "name": "María García",
  "skills": ["Python", "FastAPI", "React", "SQL"],
  "experience": [
    {
      "company": "Tech Corp",
      "position": "Backend Developer",
      "dates": "2020-2023",
      "description": "Developed REST APIs with Python and FastAPI"
    }
  ],
  "education": [
    {
      "institution": "Universidad Nacional",
      "degree": "Computer Science",
      "year": "2019"
    }
  ],
  "raw_text": "Full CV text..."
}
```

**Job Description JSON:**
```json
{
  "jd_id": "JD001",
  "title": "Senior Backend Developer",
  "must_have_requirements": ["Python 3+ years", "FastAPI", "PostgreSQL"],
  "nice_to_have": ["React", "Docker", "AWS"],
  "description": "We are looking for a Senior Backend Developer...",
  "experience_years_required": 3,
  "raw_text": "Full JD text..."
}
```

## 🧪 Testing

### Ejecutar Todos los Tests

```bash
# Opción 1: Script Python
python run_all_tests.py

# Opción 2: Script PowerShell
.\run_all_tests.ps1
```

### Tests Incluidos

1. **Verificación de Configuración** - Valida setup completo
2. **Test LLM Rápido** - Conexión básica con Gemini
3. **Test LLM Completo** - Análisis de matching
4. **Test API Principal** - 9 endpoints
5. **Test API PDF** - Procesamiento de PDF resume

### Tests Individuales

```bash
# Verificar setup
python tests/verify_setup.py

# Test LLM
python tests/test_llm_quick.py
python tests/test_llm_connection.py

# Test API
python tests/test_api.py
python tests/test_api_pdf_resume.py
```

## 📊 API Endpoints

### Health & Docs
- `GET /` - Health check
- `GET /docs` - Swagger UI

### Upload
- `POST /api/upload/resumes` - Upload resumes (PDF/JSON/TXT)
- `POST /api/upload/job-description` - Upload job description (PDF/JSON/TXT)

### Processing
- `POST /api/process` - Start analysis
  ```json
  {
    "resume_files": ["file1.json", "file2.pdf"],
    "jd_file": "job.json"
  }
  ```
- `GET /api/process/status` - Get processing status
- `GET /api/results` - Get ranked results

### Storage
- `GET /api/storage/resumes` - List stored resumes
- `GET /api/storage/job-descriptions` - List stored JDs
- `DELETE /api/storage/{file_id}` - Delete file

### Export
- `GET /api/export/csv` - Export results to CSV

## 🎨 Características Principales

### Backend Features

✅ **LLM Analysis**
- Análisis profundo de experiencia y skills
- Evaluación de fit con job requirements
- Generación de reason codes explicativos

✅ **Hybrid Scoring**
- 60% Similarity Score (semantic matching)
- 30% Must-Have Hits (rule-based)
- 10% Recency Boost (recent experience)

✅ **PDF Processing**
- Extracción de texto de CVs en PDF
- Validación de tamaño (max 50MB)
- Fallback a texto plano si falla

✅ **Text File Processing**
- Soporte para archivos .txt de job descriptions y resumes
- Codificación UTF-8 con fallback a latin-1
- Parsing inteligente de secciones estructuradas

✅ **Explainability**
- Reason codes detallados por candidato
- Hit mapper para matched requirements
- Secciones de resume identificadas

### Frontend Features

✅ **File Upload**
- Drag & drop de archivos
- Preview de archivos subidos
- Soporte PDF, JSON y TXT

✅ **Job Descriptions View** (Nuevo)
- Grid de tarjetas de JDs
- Vista detallada por JD
- Candidatos rankeados con scores visuales
- Top 3 con badges dorado/plata/bronce

✅ **Real-time Processing**
- Progress bar con porcentaje
- Tiempo estimado restante
- Actualización en tiempo real

✅ **Results Dashboard**
- Tabla de candidatos rankeados
- Scores detallados
- Export a CSV

## 🔧 Configuración Avanzada

### Cambiar Modelo LLM

```env
# Usar Gemini Pro
LLM_MODEL=gemini-1.5-pro

# Ajustar temperatura (0.0 - 1.0)
LLM_TEMPERATURE=0.5

# Aumentar max tokens
LLM_MAX_TOKENS=4000
```

### Ajustar Scoring Weights

```env
# Priorizar similarity
SCORE_WEIGHT_SIMILARITY=0.7
SCORE_WEIGHT_MUST_HAVE=0.2
SCORE_WEIGHT_RECENCY=0.1
```

### Configurar Cache

```env
# Habilitar cache de respuestas LLM
ENABLE_CACHE=true
CACHE_TTL=7200  # 2 horas
```

## 🐛 Troubleshooting

### Backend no inicia

1. Verificar Python version: `python --version` (debe ser 3.12+)
2. Verificar dependencias: `pip list`
3. Verificar .env: `python tests/verify_setup.py`
4. Revisar logs en consola

### LLM falla

1. Verificar API key válida en `.env`
2. Revisar límites de rate de Gemini API
3. Verificar conexión a internet
4. Logs mostrarán "ERROR: Analysis failed" - esto es normal, el sistema continúa con rule-based scoring

### Frontend no se conecta

1. Verificar backend corriendo: `http://localhost:8000`
2. Verificar proxy en `vite.config.mts`
3. Verificar `.env.local` con `VITE_API_BASE_URL`
4. Revisar errores de CORS en consola

### PDF no se procesa

1. Verificar tamaño < 50MB
2. Verificar que sea un PDF válido
3. Revisar logs del backend
4. Probar con JSON como alternativa

## 📚 Documentación Adicional

- [Backend README](README_BACKEND.md) - Detalles del backend
- [Frontend README](FrontEnd/README_FRONTEND.md) - Detalles del frontend
- [Setup Guide](SETUP.md) - Guía detallada de instalación
- [Quickstart](QUICKSTART.md) - Inicio rápido
- [Resume Formats](RESUME_FORMATS.md) - Formatos de CV soportados
- [TXT Support](TXT_SUPPORT.md) - Documentación de soporte para archivos .txt
- [JD Formats](JOB_DESCRIPTION_FORMATS.md) - Formatos de JD soportados
- [Tests README](tests/README.md) - Documentación de tests

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Add nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📝 Changelog

### v1.0.0 (2025-01-06)
- ✨ Implementación inicial del backend con FastAPI
- ✨ Integración con Google Gemini LLM
- ✨ Frontend React con Material-UI
- ✨ Sistema de scoring híbrido
- ✨ Procesamiento de PDFs, JSON y archivos TXT
- ✨ Nueva vista: Job Descriptions con candidatos rankeados
- ✨ Suite completa de tests
- 📚 Documentación completa

## 👥 Equipo

**Hackatón Equipo E**

## 📄 Licencia

Este proyecto fue desarrollado como parte de un hackatón.

---

**🚀 ¡Buena suerte con el matching!**
