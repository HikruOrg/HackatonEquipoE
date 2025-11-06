# Soporte para Archivos de Texto (.txt)

## Resumen

El backend ahora soporta archivos de texto plano (`.txt`) para job descriptions y resumes, además de los formatos PDF y JSON que ya estaban soportados.

## Cambios Realizados

### 1. `src/pdf_processing/pdf_validator.py`

Se agregaron los siguientes métodos:

- **`is_txt(file_path)`**: Verifica si un archivo es un archivo `.txt`
- **`validate_txt(file_path)`**: Valida archivos `.txt` con las siguientes verificaciones:
  - Existencia del archivo
  - Extensión correcta
  - Tamaño máximo de 10MB
  - Lectura correcta del archivo (prueba con UTF-8 y fallback a latin-1)

También se actualizó el método `validate_files()` para incluir validación de archivos `.txt`.

### 2. `src/pdf_processing/pdf_extractor.py`

Se agregaron los siguientes métodos:

- **`extract_text_from_txt(txt_path)`**: Extrae texto de un archivo `.txt`
  - Intenta primero con codificación UTF-8
  - Si falla, usa latin-1 como fallback
  - Registra warnings apropiados
  
- **`extract_text_from_txt_with_metadata(txt_path)`**: Extrae texto y metadatos
  - Retorna el texto y metadatos del archivo (nombre, tamaño, páginas=1)

También se modificó el constructor `__init__()` para aceptar un parámetro opcional `require_pdfplumber=True` que permite usar el extractor solo para archivos TXT sin requerir la instalación de pdfplumber.

### 3. `src/main.py`

Se actualizaron los siguientes endpoints y funciones:

- **`upload_resumes()`**: Ahora acepta archivos `.txt` además de PDF y JSON
- **`upload_job_description()`**: Ahora acepta archivos `.txt` además de PDF y JSON
- **`process_resume_file()`**: Procesa archivos `.txt` extrayendo el texto y parseándolo
- **`process_jd_file()`**: Procesa job descriptions en formato `.txt`

## Uso

### API Endpoints

Los endpoints de la API ahora aceptan archivos `.txt`:

```bash
# Subir un job description en formato TXT
curl -X POST "http://localhost:8000/api/upload/job-description" \
  -F "file=@job_description.txt"

# Subir resumes en formato TXT
curl -X POST "http://localhost:8000/api/upload/resumes" \
  -F "files=@resume1.txt" \
  -F "files=@resume2.txt"
```

### Procesamiento Local

También se puede procesar archivos `.txt` directamente desde la carpeta `data/job_descriptions/raw/`:

```python
from src.pdf_processing import PDFExtractor, PDFValidator
from src.preprocessing import JDParser

# Validar archivo TXT
validator = PDFValidator()
is_valid, error = validator.validate_txt("data/job_descriptions/raw/job.txt")

# Extraer texto
extractor = PDFExtractor(require_pdfplumber=False)
text_data = extractor.extract_text_from_txt_with_metadata("data/job_descriptions/raw/job.txt")

# Parsear job description
parser = JDParser()
jd_data = parser.parse_from_text(text_data["text"])
```

## Formato Recomendado para Archivos TXT

Para obtener mejores resultados al parsear archivos `.txt`, se recomienda el siguiente formato:

```
[Título del Puesto]

[Descripción general]

Must Have Requirements:
- Requisito 1
- Requisito 2
- Requisito 3

Nice to Have:
- Requisito opcional 1
- Requisito opcional 2

[Descripción detallada del puesto y responsabilidades]

[Información adicional]
```

### Ejemplo

```
Senior Software Engineer - Python

We are looking for an experienced Python developer to join our team.

Must Have Requirements:
- 5+ years of experience in Python development
- Strong knowledge of FastAPI or Django frameworks
- Experience with RESTful API design and development
- Proficiency in SQL and database design (PostgreSQL, MySQL)

Nice to Have:
- Experience with React or modern frontend frameworks
- Knowledge of Docker and Kubernetes
- AWS or Azure cloud platform experience

As a Senior Software Engineer, you will be responsible for designing, developing, 
and maintaining high-quality software solutions...
```

## Validación y Limitaciones

- **Tamaño máximo**: 10MB
- **Codificación**: UTF-8 (con fallback a latin-1)
- **Formatos soportados**: `.txt`, `.pdf`, `.json`

## Testing

Se creó un script de prueba `test_txt_support.py` que valida:

1. Validación de archivos `.txt`
2. Extracción de texto desde archivos `.txt`
3. Parsing de job descriptions desde texto

Para ejecutar las pruebas:

```bash
python test_txt_support.py
```

## Ejemplo de Archivo de Prueba

Se creó un archivo de ejemplo en `data/job_descriptions/raw/test_job.txt` que demuestra el formato recomendado.

## Notas Técnicas

- El parser intenta extraer automáticamente:
  - Título del puesto (primeras líneas que contienen palabras clave como "developer", "engineer", etc.)
  - Requisitos obligatorios (secciones con "must have", "required", "essential")
  - Requisitos opcionales (secciones con "nice to have", "preferred", "bonus")
  - Años de experiencia requeridos (patrones como "5+ years", "3 years experience")
  
- Si no se encuentra estructura, el parser usa heurísticas para extraer información relevante basándose en palabras clave comunes de tecnologías y habilidades.

## Compatibilidad

Esta actualización es completamente retrocompatible. Los archivos PDF y JSON existentes continúan funcionando exactamente como antes.
