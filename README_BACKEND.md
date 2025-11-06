# AI Talent Matcher Backend

Backend API para el sistema AI Talent Matcher que analiza y rankea candidatos contra descripciones de trabajo usando LLMs.

## Características

- ✅ Procesamiento de PDFs y JSONs
- ✅ Extracción de texto de PDFs
- ✅ Parsing inteligente de resumes y job descriptions
- ✅ Análisis con LLM usando LangChain
- ✅ Sistema de scoring híbrido (similaridad + reglas)
- ✅ Generación de reason codes explicables
- ✅ Storage local para JSONs procesados
- ✅ Exportación a CSV
- ✅ API REST con FastAPI

## Requisitos

- Python 3.9+
- pip

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env y agregar tu API key de OpenAI o el proveedor LLM que uses
```

## Configuración

Edita el archivo `.env` con tus credenciales:

- `LLM_PROVIDER`: openai, gemini, anthropic, o ollama
- `OPENAI_API_KEY`: Tu API key de OpenAI (si usas OpenAI)
- `OPENAI_MODEL`: Modelo a usar (gpt-4-turbo-preview, gpt-3.5-turbo, etc.)

## Uso

### Ejecutar el servidor API

```bash
python -m src.main
# O usando uvicorn directamente:
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en `http://localhost:8000`

### Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints principales

- `POST /api/upload/resumes` - Subir archivos de resumes (PDF o JSON)
- `POST /api/upload/job-description` - Subir job description (PDF o JSON)
- `POST /api/process` - Iniciar procesamiento
- `GET /api/process/status` - Estado del procesamiento
- `GET /api/results` - Obtener resultados rankeados
- `GET /api/results/{candidate_id}` - Detalles de un candidato
- `GET /api/storage/resumes` - Listar resumes almacenados
- `GET /api/storage/job-descriptions` - Listar JDs almacenados
- `GET /api/storage/search` - Buscar en storage
- `GET /api/export/csv` - Exportar resultados a CSV

## Estructura del Proyecto

```
src/
├── pdf_processing/     # Extracción y validación de PDFs
├── preprocessing/      # Parsing de resumes y JDs
├── llm/               # Cliente LLM y análisis
├── prompts/           # Gestión de prompts
├── scoring/           # Sistema de scoring híbrido
├── storage/           # Storage local/cloud
├── export/            # Exportación a CSV
├── explainability/    # Reason codes y mapeo de hits
├── config.py          # Configuración
└── main.py            # API FastAPI

data/
├── resumes/           # Resumes de entrada
├── job_descriptions/ # JDs de entrada
├── storage/          # JSONs almacenados
├── cache/            # Cache de procesamiento
└── output/           # CSVs exportados
```

## Desarrollo

### Ejecutar tests

```bash
pytest tests/
```

### Formatear código

```bash
black src/
```

### Linting

```bash
flake8 src/
```

## Notas

- El sistema usa LangChain para abstraer las diferentes APIs de LLM
- Los prompts están en `src/prompts/` y pueden ser modificados
- El storage por defecto es local, pero puede extenderse para cloud storage
- Los resultados se rankean automáticamente por score final

## Licencia

Ver archivo LICENSE

