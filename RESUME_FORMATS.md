# 📄 Formatos de Entrada para Resumes/CVs

## Formatos Aceptados

El backend acepta **2 formatos** para Resumes/CVs en la carpeta `data/resumes/raw/`:

### 1. PDF (.pdf) ✅
- **Extensión**: `.pdf`
- **Tamaño máximo**: 50 MB
- **Validación**: Header PDF válido (`%PDF`)
- **Procesamiento**: El texto se extrae automáticamente con `pdfplumber`

**Ejemplo de uso:**
```
data/resumes/raw/john_doe_resume.pdf
data/resumes/raw/maria_garcia_cv_2024.pdf
```

### 2. JSON (.json) ✅
- **Extensión**: `.json`
- **Tamaño máximo**: 10 MB
- **Validación**: JSON válido con estructura específica
- **Procesamiento**: Se parsea directamente

---

## Estructura JSON Requerida

### Campos Obligatorios:
```json
{
  "candidate_id": "string (único)",
  "name": "string",
  "skills": {}, 
  "experience": [],
  "education": [],
  "raw_text": "string (texto completo del CV)"
}
```

### Ejemplo Completo:
```json
{
  "candidate_id": "CAND001",
  "name": "María García López",
  "email": "maria.garcia@example.com",
  "phone": "+34 600 123 456",
  "summary": "Desarrolladora Full Stack con 5 años de experiencia en Python y JavaScript.",
  "experience": [
    {
      "title": "Senior Python Developer",
      "company": "Tech Solutions S.A.",
      "location": "Madrid, España",
      "start_date": "2021-03",
      "end_date": "2024-10",
      "duration": "3 años 7 meses",
      "responsibilities": [
        "Desarrollo de APIs REST con FastAPI",
        "Implementación de microservicios con Docker",
        "Diseño de bases de datos PostgreSQL"
      ],
      "technologies": ["Python", "FastAPI", "Django", "PostgreSQL", "Docker"]
    },
    {
      "title": "Full Stack Developer",
      "company": "Digital Innovation Lab",
      "location": "Barcelona, España",
      "start_date": "2019-06",
      "end_date": "2021-02",
      "duration": "1 año 8 meses",
      "responsibilities": [
        "Desarrollo frontend con React",
        "Backend con Python y Flask"
      ],
      "technologies": ["Python", "Flask", "React", "TypeScript"]
    }
  ],
  "education": [
    {
      "degree": "Máster en Ingeniería de Software",
      "institution": "Universidad Politécnica de Madrid",
      "location": "Madrid, España",
      "graduation_date": "2019",
      "field": "Ingeniería de Software"
    }
  ],
  "skills": {
    "programming_languages": ["Python", "JavaScript", "TypeScript", "SQL"],
    "frameworks": ["FastAPI", "Django", "Flask", "React"],
    "databases": ["PostgreSQL", "MongoDB", "Redis"],
    "tools": ["Docker", "Git", "AWS"]
  },
  "certifications": [
    {
      "name": "AWS Certified Solutions Architect",
      "issuer": "Amazon Web Services",
      "date": "2023-06"
    }
  ],
  "languages": [
    {
      "language": "Español",
      "proficiency": "Nativo"
    },
    {
      "language": "Inglés",
      "proficiency": "Avanzado (C1)"
    }
  ],
  "raw_text": "María García López\nmaria.garcia@example.com\n\nDesarrolladora Full Stack con 5 años de experiencia...\n\nEXPERIENCIA\nSenior Python Developer - Tech Solutions (2021-2024)\n...\n\nEDUCACIÓN\nMáster en Ingeniería de Software - UPM (2019)"
}
```

### Campos Opcionales:
- `email` - Email del candidato
- `phone` - Teléfono de contacto
- `summary` - Resumen profesional
- `certifications` - Certificaciones obtenidas
- `languages` - Idiomas que habla
- `location` - Ubicación actual
- `linkedin` - Perfil de LinkedIn
- `github` - Perfil de GitHub
- `website` - Sitio web personal

---

## Validación

### PDF
✅ Debe tener extensión `.pdf`  
✅ Debe tener header válido (`%PDF`)  
✅ Tamaño máximo: 50 MB  
✅ Debe ser legible

### JSON
✅ Debe tener extensión `.json`  
✅ Debe ser JSON válido (parseable)  
✅ Tamaño máximo: 10 MB  
✅ **Debe incluir campos obligatorios**:
   - `candidate_id`
   - `name`
   - `skills`
   - `experience`
   - `education`
   - `raw_text`

---

## Procesamiento

### Flujo PDF:
1. **Upload** → El PDF se sube al servidor
2. **Extracción** → `pdfplumber` extrae el texto
3. **Parsing** → `ResumeParser` estructura el texto
4. **Validación** → Se verifica la estructura
5. **Storage** → Se guarda como JSON en `data/storage/resumes/`

### Flujo JSON:
1. **Upload** → El JSON se sube al servidor
2. **Validación** → Se verifica que tenga los campos requeridos
3. **Parsing** → `ResumeParser` valida la estructura
4. **Storage** → Se guarda en `data/storage/resumes/`

---

## Ejemplos de Archivos Válidos

### ✅ PDF Válido:
```
data/resumes/raw/
├── maria_garcia_cv.pdf
├── john_smith_resume_2024.pdf
└── candidate_123.pdf
```

### ✅ JSON Válido:
```
data/resumes/raw/
├── test_resume.json
├── developer_profile.json
└── senior_engineer.json
```

### ❌ Archivos NO Soportados:
```
❌ resume.docx (Word)
❌ cv.txt (Texto plano sin extensión .json)
❌ profile.xlsx (Excel)
❌ resume.html (HTML)
❌ cv.xml (XML)
```

---

## Ejemplo de Uso con API

### Subir PDF:
```bash
curl -X POST "http://localhost:8000/api/upload/resumes" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@data/resumes/raw/maria_garcia_cv.pdf"
```

### Subir múltiples archivos:
```bash
curl -X POST "http://localhost:8000/api/upload/resumes" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@data/resumes/raw/cv1.pdf" \
  -F "files=@data/resumes/raw/cv2.json" \
  -F "files=@data/resumes/raw/cv3.pdf"
```

### Respuesta Exitosa:
```json
{
  "uploaded": 3,
  "files": [
    {
      "filename": "cv1.pdf",
      "path": "/tmp/tmpXXXXXX.pdf",
      "type": "pdf"
    },
    {
      "filename": "cv2.json",
      "path": "/tmp/tmpYYYYYY.json",
      "type": "json"
    },
    {
      "filename": "cv3.pdf",
      "path": "/tmp/tmpZZZZZZ.pdf",
      "type": "pdf"
    }
  ],
  "errors": []
}
```

---

## Errores Comunes

### Error: "Unsupported file type"
**Causa**: El archivo no es `.pdf` ni `.json`  
**Solución**: Convierte el archivo a PDF o JSON

### Error: "Invalid PDF header"
**Causa**: El archivo tiene extensión `.pdf` pero no es un PDF válido  
**Solución**: Verifica que el archivo sea un PDF real

### Error: "Invalid JSON format"
**Causa**: El JSON tiene errores de sintaxis  
**Solución**: Valida el JSON con un validador online (jsonlint.com)

### Error: "Invalid resume JSON structure"
**Causa**: Faltan campos obligatorios en el JSON  
**Solución**: Agrega los campos requeridos:
- `candidate_id`
- `name`
- `skills`
- `experience`
- `education`
- `raw_text`

### Error: "File too large"
**Causa**: El archivo excede el tamaño máximo  
**Solución**: 
- PDF: Reduce el tamaño a menos de 50 MB
- JSON: Reduce el tamaño a menos de 10 MB

---

## Ubicaciones de Archivos

```
data/
└── resumes/
    ├── raw/              ← Coloca tus archivos aquí (PDF o JSON)
    ├── processed/        ← JSONs procesados (generados automáticamente)
    └── ../storage/
        └── resumes/      ← Storage final (generado automáticamente)
```

---

## Resumen Rápido

| Formato | Extensión | Tamaño Máx | Campos Requeridos |
|---------|-----------|------------|-------------------|
| PDF | `.pdf` | 50 MB | Ninguno (se extrae) |
| JSON | `.json` | 10 MB | 6 campos obligatorios |

**Formatos soportados**: ✅ PDF, ✅ JSON  
**Formatos NO soportados**: ❌ Word, ❌ Excel, ❌ TXT plano, ❌ HTML, ❌ XML

---

## Consejos para Mejores Resultados

### Para PDFs:
- ✅ Usa PDFs con texto seleccionable (no imágenes escaneadas)
- ✅ Estructura clara con secciones bien definidas
- ✅ Evita diseños muy complejos con múltiples columnas
- ✅ Usa fuentes estándar y legibles

### Para JSONs:
- ✅ Incluye toda la información relevante en `raw_text`
- ✅ Usa arrays para listas (experience, education, skills)
- ✅ Formatos de fecha consistentes (YYYY-MM o YYYY-MM-DD)
- ✅ Categoriza las habilidades por tipo
- ✅ Incluye tecnologías específicas en cada experiencia

### Para Matching Óptimo:
- ✅ Menciona tecnologías específicas (Python, FastAPI, etc.)
- ✅ Incluye años de experiencia
- ✅ Detalla proyectos y responsabilidades
- ✅ Agrega certificaciones relevantes
- ✅ Menciona metodologías (Agile, Scrum, etc.)
