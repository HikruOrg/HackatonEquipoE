# ⚡ Inicio Rápido - Backend AI Talent Matcher

## 🎯 Configuración Rápida (5 minutos)

### Paso 1: Configurar API Key
Edita el archivo `.env` y agrega tu API key de OpenAI:
```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

**¿No tienes API key?** Obtén una gratis en: https://platform.openai.com/api-keys

### Paso 2: Crear Entorno Virtual
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si obtienes error de permisos:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Paso 3: Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### Paso 4: Verificar Configuración
```powershell
python verify_setup.py
```

### Paso 5: Iniciar Servidor
```powershell
python run_server.py
```

¡Listo! Visita http://localhost:8000/docs para ver la API.

---

## 🔧 Comandos Útiles

### Activar entorno virtual
```powershell
.\venv\Scripts\Activate.ps1
```

### Desactivar entorno virtual
```powershell
deactivate
```

### Reiniciar servidor
```powershell
# Ctrl+C para detener
python run_server.py
```

### Ver logs del servidor
Los logs se muestran en la consola donde ejecutaste `run_server.py`

---

## 📚 Documentación Completa

- **SETUP.md** - Guía completa de configuración
- **README_BACKEND.md** - Documentación del backend
- **docs/PROJECT_GUIDELINES.md** - Guías del proyecto

---

## 🆘 ¿Problemas?

### Error: "Module not found"
```powershell
pip install -r requirements.txt --force-reinstall
```

### Error: "Cannot execute scripts"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Port already in use"
```powershell
# Usa otro puerto
uvicorn src.main:app --reload --port 8001
```

### API Key no funciona
1. Verifica que copiaste la key completa
2. Verifica que empiece con `sk-`
3. Reinicia el servidor después de cambiar `.env`

---

## 🌟 Alternativas Gratuitas a OpenAI

### Opción 1: Ollama (100% Local y Gratis)
```powershell
# Instalar Ollama: https://ollama.ai/
# Descargar modelo
ollama pull llama2

# Iniciar servidor
ollama serve

# En .env cambiar:
# LLM_PROVIDER=ollama
```

### Opción 2: Google Gemini (API Gratuita)
```powershell
# Obtener API key: https://makersuite.google.com/app/apikey
# En .env cambiar:
# LLM_PROVIDER=gemini
# GOOGLE_API_KEY=tu-key-aqui
```

---

## 📊 Siguiente Paso

Una vez que el servidor esté corriendo:
1. Visita http://localhost:8000/docs
2. Prueba el endpoint `/api/upload/resumes`
3. Sube algunos CVs en formato PDF o JSON
4. Revisa la documentación interactiva en Swagger UI
