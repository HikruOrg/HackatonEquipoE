# 🎬 Pasos para Ejecutar el Backend - AHORA

## ✅ Lo que ya está listo:
- ✅ Archivo `.env` creado (necesitas agregar tu API key)
- ✅ Archivo `.env.example` creado
- ✅ Archivo `.gitignore` configurado
- ✅ Scripts de verificación y ejecución listos
- ✅ Python 3.12.10 instalado

## 🚀 Ejecuta estos comandos en orden:

### 1️⃣ Crear entorno virtual
```powershell
python -m venv venv
```

### 2️⃣ Activar entorno virtual
```powershell
.\venv\Scripts\Activate.ps1
```

**Si obtienes error de permisos**, ejecuta primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Luego vuelve a intentar activar el entorno.

### 3️⃣ Actualizar pip (recomendado)
```powershell
python -m pip install --upgrade pip
```

### 4️⃣ Instalar dependencias
```powershell
pip install -r requirements.txt
```
*Esto tomará 2-3 minutos*

### 5️⃣ Configurar API Key

**Edita el archivo `.env`** y cambia esta línea:
```env
OPENAI_API_KEY=
```

Por tu API key real:
```env
OPENAI_API_KEY=sk-tu-api-key-completa-aqui
```

**¿Dónde obtener tu API key?**
1. Ve a: https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Haz clic en "Create new secret key"
4. Copia la key (empieza con `sk-`)
5. Pégala en el archivo `.env`

**¿No quieres usar OpenAI?** Usa Ollama gratis:
1. Descarga Ollama: https://ollama.ai/
2. Ejecuta: `ollama pull llama2`
3. Ejecuta: `ollama serve`
4. En `.env` cambia: `LLM_PROVIDER=ollama`

### 6️⃣ Verificar configuración
```powershell
python verify_setup.py
```

### 7️⃣ Iniciar el servidor
```powershell
python run_server.py
```

### 8️⃣ Probar el servidor

Abre tu navegador en:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

---

## 📝 Notas importantes:

1. **Mantén el entorno virtual activado**: Verás `(venv)` al inicio de tu línea de comando
2. **Si cierras la terminal**: Necesitas reactivar el entorno con `.\venv\Scripts\Activate.ps1`
3. **Para detener el servidor**: Presiona `Ctrl+C`
4. **Los logs aparecen en consola**: Revísalos si algo falla

---

## 🔍 Verificación rápida:

Después de instalar, verifica que todo funcione:
```powershell
# Dentro del entorno virtual (venv)
python -c "import fastapi, langchain, pdfplumber; print('✅ Todo OK')"
```

---

## 🆘 Si algo falla:

1. **Error de módulos**: `pip install -r requirements.txt --force-reinstall`
2. **Puerto ocupado**: Cambia el puerto en `run_server.py` (línea 7: `port=8001`)
3. **API Key inválida**: Revisa que la copiaste completa desde OpenAI
4. **Entorno virtual no activa**: Revisa que veas `(venv)` al inicio de tu terminal

---

## 📞 Estado actual:
- Python: ✅ 3.12.10
- Entorno virtual: ❌ Necesitas crearlo (paso 1)
- Dependencias: ❌ Necesitas instalarlas (paso 4)
- API Key: ⚠️ Necesitas configurarla (paso 5)
- Servidor: ⏸️ Listo para iniciar (paso 7)
