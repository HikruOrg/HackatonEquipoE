# 🚀 Guía de Configuración del Backend - AI Talent Matcher

## 📋 Pasos para Configuración

### 1. Variables de Entorno

Hemos creado los siguientes archivos:
- **`.env.example`** - Plantilla con todas las variables disponibles
- **`.env`** - Archivo real de configuración (ya creado, necesitas editarlo)

### 2. Configurar tu Proveedor LLM

Elige **UNO** de estos proveedores y configura su API key:

#### Opción A: OpenAI (Recomendado) 🌟
1. Visita: https://platform.openai.com/api-keys
2. Crea una cuenta o inicia sesión
3. Genera una nueva API key
4. En el archivo `.env`, actualiza:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-tu-api-key-aqui
   ```

#### Opción B: Google Gemini
1. Visita: https://makersuite.google.com/app/apikey
2. Genera tu API key
3. En el archivo `.env`, actualiza:
   ```env
   LLM_PROVIDER=gemini
   GOOGLE_API_KEY=tu-api-key-aqui
   ```

#### Opción C: Anthropic Claude
1. Visita: https://console.anthropic.com/
2. Genera tu API key
3. En el archivo `.env`, actualiza:
   ```env
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=tu-api-key-aqui
   ```

#### Opción D: Ollama (Local, Gratis) 🆓
1. Instala Ollama: https://ollama.ai/
2. Descarga un modelo: `ollama pull llama2`
3. Inicia el servidor: `ollama serve`
4. En el archivo `.env`, actualiza:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

### 3. Instalar Dependencias de Python

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Si hay problemas con la ejecución de scripts, ejecuta:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Verificar la Instalación

```powershell
# Verificar que Python encuentra los módulos
python -c "import fastapi, langchain, pdfplumber; print('✅ Dependencias instaladas correctamente')"
```

### 5. Iniciar el Servidor

```powershell
# Opción 1: Usando el script
python run_server.py

# Opción 2: Usando uvicorn directamente
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Probar la API

Una vez iniciado el servidor, visita:
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Alternativa (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

## 🔧 Solución de Problemas Comunes

### Error: "Module not found"
```powershell
# Asegúrate de que el entorno virtual está activado
.\venv\Scripts\Activate.ps1

# Reinstala las dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "API key not configured"
- Verifica que el archivo `.env` existe en la raíz del proyecto
- Verifica que la API key está correctamente configurada
- Reinicia el servidor después de cambiar el `.env`

### Error: "Cannot execute scripts"
```powershell
# Permite la ejecución de scripts en PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Puerto 8000 en uso
```powershell
# Usa un puerto diferente
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

## 📁 Estructura de Datos

El sistema creará automáticamente estas carpetas al iniciar:
```
data/
├── cache/              # Cache de respuestas LLM y embeddings
├── output/             # CSVs exportados
├── storage/            # JSONs procesados
│   ├── resumes/
│   └── job_descriptions/
├── resumes/
│   ├── raw/           # PDFs de resumes originales
│   └── processed/     # JSONs procesados
└── job_descriptions/
    ├── raw/           # PDFs de JDs originales
    └── processed/     # JSONs procesados
```

## 🎯 Siguiente Paso

Una vez configurado el backend, prueba estos comandos:

```powershell
# 1. Iniciar el servidor
python run_server.py

# 2. En otra terminal, prueba la API
curl http://localhost:8000/

# 3. Visita la documentación interactiva
# Abre en tu navegador: http://localhost:8000/docs
```

## 📊 Configuración de Scoring

Los pesos del sistema de scoring deben sumar 1.0:
- **SIMILARITY_WEIGHT**: 0.6 (60% - Similaridad general)
- **MUST_HAVE_BOOST_WEIGHT**: 0.3 (30% - Requisitos obligatorios)
- **RECENCY_BOOST_WEIGHT**: 0.1 (10% - Experiencia reciente)

Puedes ajustar estos valores en el archivo `.env`.

## 🔐 Seguridad

- **Nunca** subas el archivo `.env` al repositorio
- El `.gitignore` ya está configurado para ignorar `.env`
- Usa `.env.example` como referencia para otros desarrolladores
- Rota tus API keys regularmente

## 📞 Soporte

Si encuentras problemas:
1. Verifica que todas las dependencias estén instaladas
2. Revisa los logs del servidor
3. Verifica que el archivo `.env` esté bien configurado
4. Asegúrate de tener una API key válida
