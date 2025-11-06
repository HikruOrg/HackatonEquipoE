#!/usr/bin/env python3
"""Script to verify backend configuration and dependencies."""
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.9+")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    required = [
        "fastapi",
        "uvicorn",
        "pdfplumber",
        "langchain",
        "pandas",
        "dotenv",
    ]
    
    missing = []
    for package in required:
        try:
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - no instalado")
            missing.append(package)
    
    return len(missing) == 0

def check_env_file():
    """Check if .env file exists."""
    env_path = Path(".env")
    if env_path.exists():
        print("✅ Archivo .env encontrado")
        return True
    else:
        print("❌ Archivo .env no encontrado")
        print("   Copia .env.example a .env y configura tus API keys")
        return False

def check_env_variables():
    """Check if required environment variables are set."""
    from dotenv import load_dotenv
    load_dotenv()
    
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    print(f"📝 LLM_PROVIDER: {llm_provider}")
    
    if llm_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key and api_key != "your_openai_api_key_here" and api_key != "":
            print(f"✅ OPENAI_API_KEY configurada (primeros 10 caracteres: {api_key[:10]}...)")
            return True
        else:
            print("❌ OPENAI_API_KEY no configurada o usa valor por defecto")
            return False
    
    elif llm_provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if api_key and api_key != "your_google_api_key_here" and api_key != "":
            print(f"✅ GOOGLE_API_KEY configurada")
            return True
        else:
            print("❌ GOOGLE_API_KEY no configurada")
            return False
    
    elif llm_provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if api_key and api_key != "your_anthropic_api_key_here" and api_key != "":
            print(f"✅ ANTHROPIC_API_KEY configurada")
            return True
        else:
            print("❌ ANTHROPIC_API_KEY no configurada")
            return False
    
    elif llm_provider == "ollama":
        print("ℹ️  Usando Ollama (local) - No se requiere API key")
        print("   Asegúrate de que Ollama esté corriendo: ollama serve")
        return True
    
    return True

def check_directories():
    """Check if required directories exist."""
    dirs = [
        "data/cache",
        "data/output",
        "data/storage",
        "data/resumes/raw",
        "data/resumes/processed",
        "data/job_descriptions/raw",
        "data/job_descriptions/processed",
    ]
    
    all_exist = True
    for dir_path in dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"ℹ️  {dir_path}/ - será creado automáticamente")
    
    return True

def check_config_module():
    """Try to import and validate config."""
    try:
        from src.config import config
        config.validate()
        print("✅ Configuración validada correctamente")
        return True
    except ValueError as e:
        print(f"⚠️  Advertencia de configuración: {e}")
        print("   El servidor iniciará pero algunas funciones no estarán disponibles")
        return False
    except Exception as e:
        print(f"❌ Error al cargar configuración: {e}")
        return False

def main():
    """Run all checks."""
    print("=" * 60)
    print("🔍 Verificando Configuración del Backend")
    print("=" * 60)
    print()
    
    print("📦 Verificando Python:")
    python_ok = check_python_version()
    print()
    
    print("📚 Verificando Dependencias:")
    deps_ok = check_dependencies()
    print()
    
    print("📁 Verificando Archivos de Configuración:")
    env_file_ok = check_env_file()
    print()
    
    if env_file_ok:
        print("🔑 Verificando Variables de Entorno:")
        env_vars_ok = check_env_variables()
        print()
    else:
        env_vars_ok = False
    
    print("📂 Verificando Estructura de Directorios:")
    dirs_ok = check_directories()
    print()
    
    print("⚙️  Verificando Módulo de Configuración:")
    config_ok = check_config_module()
    print()
    
    print("=" * 60)
    if python_ok and deps_ok and env_file_ok and env_vars_ok and dirs_ok:
        print("✅ ¡Todo listo! Puedes iniciar el servidor:")
        print("   python run_server.py")
    elif python_ok and deps_ok and env_file_ok and dirs_ok:
        print("⚠️  Configuración parcial. El servidor puede iniciar pero:")
        print("   - Configura tu API key en el archivo .env")
        print("   - Las funciones LLM no funcionarán sin API key")
        print()
        print("   Puedes iniciar el servidor de todos modos:")
        print("   python run_server.py")
    else:
        print("❌ Hay problemas que resolver:")
        if not python_ok:
            print("   - Actualiza Python a la versión 3.9 o superior")
        if not deps_ok:
            print("   - Instala las dependencias: pip install -r requirements.txt")
        if not env_file_ok:
            print("   - Crea el archivo .env: cp .env.example .env")
        if not env_vars_ok:
            print("   - Configura tu API key en el archivo .env")
    print("=" * 60)

if __name__ == "__main__":
    main()
