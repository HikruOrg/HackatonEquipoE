# Requerimientos del Proyecto - AI Talent Matcher

## 1. Requerimientos Funcionales

### RF-001: Carga Dual de Datos (PDF y JSON)
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir cargar datos tanto desde archivos PDF como desde archivos JSON, manteniendo ambas funcionalidades.

**Criterios de Aceptación:**
- [ ] Cargar múltiples archivos PDF de resumes desde interfaz de carga
- [ ] Cargar archivo PDF de Job Description desde interfaz de carga
- [ ] Cargar archivos JSON de resumes desde interfaz de carga
- [ ] Cargar archivo JSON de Job Description desde interfaz de carga
- [ ] Detectar automáticamente el formato del archivo (PDF o JSON)
- [ ] Validar formato antes de procesar
- [ ] Mostrar mensajes de error claros si el formato es inválido
- [ ] Soportar procesamiento de al menos 50 resumes simultáneamente
- [ ] Permitir mezclar PDFs y JSONs en la misma sesión de carga

**Formatos Soportados:**
- PDFs con texto nativo (preferido para PDFs)
- PDFs escaneados (requiere OCR opcional)
- Archivos JSON con estructura válida

---

### RF-002: Procesamiento de PDFs y Conversión a JSON
**Prioridad:** Alta  
**Descripción:** El sistema debe procesar PDFs y convertirlos a JSON estructurado, o trabajar directamente con JSON si ya está estructurado.

**Criterios de Aceptación:**
- [ ] Extraer texto de archivos PDF usando librería de procesamiento de PDF
- [ ] Parsear texto extraído de resumes PDF a estructura JSON
- [ ] Parsear texto extraído de Job Description PDF a estructura JSON
- [ ] Extraer campos estructurados: nombre, habilidades, experiencia, educación
- [ ] Usar LLM para estructuración inteligente del texto si es necesario
- [ ] Mantener texto crudo (`raw_text`) además de campos estructurados
- [ ] Validar estructura JSON generada antes de continuar
- [ ] Si el archivo ya es JSON, validar estructura y usar directamente
- [ ] Guardar JSON estructurado en storage (local o cloud)

**Estructura Esperada (Resume JSON):**
- `candidate_id`: ID único generado o extraído
- `name`: Nombre del candidato
- `skills`: Lista de habilidades extraídas
- `experience`: Lista de experiencias laborales con company, position, dates, description
- `education`: Lista de educación con institution, degree, field, year
- `raw_text`: Texto completo extraído del PDF

**Estructura Esperada (JD JSON):**
- `jd_id`: ID único del job description
- `title`: Título del puesto
- `must_have_requirements`: Lista de requisitos obligatorios
- `nice_to_have`: Lista de requisitos deseables (opcional)
- `description`: Descripción completa del puesto
- `experience_years_required`: Años de experiencia requeridos
- `raw_text`: Texto completo extraído del PDF

---

### RF-003: Análisis con LLM
**Prioridad:** Alta  
**Descripción:** El sistema debe usar LLMs para analizar la compatibilidad entre resumes y job descriptions.

**Criterios de Aceptación:**
- [ ] Integrar con OpenAI API (GPT-4 o GPT-3.5-turbo)
- [ ] Usar prompts definidos en `src/prompts/` para el análisis
- [ ] Generar análisis estructurado en formato JSON
- [ ] Manejar errores de API (rate limits, timeouts) con retry logic
- [ ] Procesar cada candidato de forma individual contra el JD
- [ ] Tiempo máximo de respuesta por candidato: 30 segundos

**Prompts Requeridos:**
- Prompt de scoring general
- Prompt de análisis de similitud
- Prompt de generación de reason codes

---

### RF-004: Sistema de Scoring Híbrido
**Prioridad:** Alta  
**Descripción:** El sistema debe calcular un score híbrido combinando similitud semántica y reglas específicas.

**Criterios de Aceptación:**
- [ ] Calcular score de similitud (0-100) usando análisis del LLM
- [ ] Aplicar boost por must-have requirements (0-30 puntos adicionales)
- [ ] Aplicar boost por recencia de experiencia (0-10 puntos adicionales)
- [ ] Score final debe estar en rango 0-100
- [ ] Los pesos deben ser configurables vía variables de entorno
- [ ] Fórmula: `Final Score = Similarity Score + Must-Have Boost + Recency Boost`

**Configuración por Defecto:**
- Similarity Weight: 60%
- Must-Have Boost Weight: 30%
- Recency Boost Weight: 10%

---

### RF-005: Generación de Reason Codes
**Prioridad:** Alta  
**Descripción:** El sistema debe generar códigos de razón que expliquen por qué un candidato recibió su score.

**Criterios de Aceptación:**
- [ ] Generar reason codes usando LLM para cada candidato
- [ ] Mapear reason codes a secciones específicas del resume
- [ ] Incluir referencias a líneas o secciones del resume cuando aplique
- [ ] Reason codes deben ser legibles y explicativos
- [ ] Formato: Lista de códigos con descripción (ej: `SKILL_MATCH: Python, JavaScript`, `EXPERIENCE_MATCH: 5+ years in backend`)

**Reason Codes Esperados:**
- `SKILL_MATCH`: Habilidades que coinciden con el JD
- `EXPERIENCE_MATCH`: Experiencia relevante encontrada
- `MUST_HAVE_MATCH`: Requisitos obligatorios cumplidos
- `RECENT_EXP`: Experiencia reciente (últimos 2 años)
- `EDUCATION_MATCH`: Educación relevante
- `MISSING_REQUIREMENT`: Requisitos faltantes

---

### RF-006: Ranking de Candidatos
**Prioridad:** Alta  
**Descripción:** El sistema debe rankear candidatos de mayor a menor score.

**Criterios de Aceptación:**
- [ ] Ordenar candidatos por score final descendente
- [ ] Mostrar ranking numérico (1, 2, 3...)
- [ ] En caso de empate, priorizar por must-have hits
- [ ] Mostrar top 10 candidatos por defecto con opción de ver todos

---

### RF-007: Visualización de Resultados
**Prioridad:** Alta  
**Descripción:** El sistema debe mostrar una tabla rankeada con los resultados del análisis.

**Criterios de Aceptación:**
- [ ] Mostrar tabla con columnas: Rank, Candidate ID, Name, Overall Score, Similarity Score, Must-Have Hits, Reason Codes
- [ ] Tabla debe ser responsive y legible
- [ ] Permitir ordenar por diferentes columnas (click en header)
- [ ] Mostrar tooltip o expandir detalles de reason codes al hacer hover/click
- [ ] Resaltar visualmente candidatos con score > 80
- [ ] Mostrar indicador de progreso durante el procesamiento

**Columnas de la Tabla:**
- Rank (número)
- Candidate ID
- Name
- Overall Score (0-100)
- Similarity Score (0-100)
- Must-Have Hits (número)
- Recency Boost (puntos)
- Reason Codes (lista expandible)

---

### RF-008: Exportación a CSV
**Prioridad:** Media  
**Descripción:** El sistema debe permitir exportar los resultados rankeados a formato CSV.

**Criterios de Aceptación:**
- [ ] Exportar tabla completa a CSV
- [ ] Incluir todas las columnas visibles en la tabla
- [ ] Reason codes deben estar en formato legible (separados por punto y coma)
- [ ] Archivo CSV debe guardarse en `data/output/`
- [ ] Nombre de archivo: `ranked_candidates_YYYYMMDD_HHMMSS.csv`
- [ ] Encoding UTF-8 para soportar caracteres especiales
- [ ] Botón de exportación visible en la interfaz

---

### RF-009: Mapeo de Hits a Resume
**Prioridad:** Media  
**Descripción:** El sistema debe mapear los hits encontrados a secciones específicas del resume.

**Criterios de Aceptación:**
- [ ] Para cada reason code, identificar la sección del resume relacionada
- [ ] Mostrar referencia a sección (ej: "Experience > Company X > Position Y")
- [ ] Permitir ver el texto original del resume relacionado
- [ ] Formato: `{reason_code}: {resume_section_reference}`

---

## 2. Requerimientos Técnicos

### RT-001: Arquitectura del Sistema
**Prioridad:** Alta  
**Descripción:** El sistema debe seguir la estructura de proyecto definida en INFRA_GUIDELINES.MD.

**Criterios de Aceptación:**
- [ ] Implementar estructura de directorios según especificación
- [ ] Separar responsabilidades en módulos (pdf_processing, preprocessing, storage, llm, scoring, export)
- [ ] Usar Python 3.9+ como lenguaje base
- [ ] Implementar configuración centralizada en `src/config.py`
- [ ] Incluir módulo de procesamiento de PDFs antes del análisis
- [ ] Incluir módulo de gestión de storage para JSONs

---

### RT-006: Integración con Storage
**Prioridad:** Alta  
**Descripción:** El sistema debe conectarse a un storage (local o cloud) para almacenar y recuperar JSONs.

**Criterios de Aceptación:**
- [ ] Soportar storage local (filesystem) como opción por defecto
- [ ] Soportar storage cloud (AWS S3, Azure Blob Storage, Google Cloud Storage)
- [ ] Configurar conexión a storage mediante variables de entorno
- [ ] Implementar funciones para guardar JSONs en storage
- [ ] Implementar funciones para listar JSONs disponibles en storage
- [ ] Implementar funciones para buscar JSONs por criterios (nombre, fecha, tipo)
- [ ] Implementar funciones para recuperar JSONs desde storage
- [ ] Implementar funciones para eliminar JSONs del storage
- [ ] Validar permisos de acceso al storage antes de operaciones
- [ ] Manejar errores de conexión al storage de forma robusta
- [ ] Implementar caché local de metadatos de JSONs para mejor performance

**Storage Options:**
- Local filesystem: `data/storage/resumes/` y `data/storage/job_descriptions/`
- AWS S3: Bucket configurable
- Azure Blob Storage: Container configurable
- Google Cloud Storage: Bucket configurable

---

### RT-002: Integración con LLM
**Prioridad:** Alta  
**Descripción:** El sistema debe integrarse correctamente con APIs de LLM.

**Criterios de Aceptación:**
- [ ] Implementar cliente LLM con retry logic usando `tenacity`
- [ ] Manejar rate limits con exponential backoff
- [ ] Validar respuestas JSON del LLM antes de procesar
- [ ] Implementar timeout de 60 segundos por request
- [ ] Loggear todos los errores de API para debugging
- [ ] Soportar configuración de modelo vía variables de entorno

---

### RT-003: Gestión de Prompts
**Prioridad:** Alta  
**Descripción:** Los prompts deben estar centralizados y ser fácilmente modificables.

**Criterios de Aceptación:**
- [ ] Almacenar prompts en `src/prompts/` o `prompts/`
- [ ] Implementar `PromptLoader` para cargar prompts desde archivos
- [ ] Soportar variables en prompts usando formato `.format()`
- [ ] Documentar cada prompt con su propósito y formato esperado
- [ ] Versionar prompts en git

**Prompts Mínimos Requeridos:**
- `scoring_prompt.txt`: Análisis general y scoring
- `similarity_prompt.txt`: Análisis de similitud
- `reason_codes_prompt.txt`: Generación de reason codes

---

### RT-004: Manejo de Errores
**Prioridad:** Media  
**Descripción:** El sistema debe manejar errores de forma robusta.

**Criterios de Aceptación:**
- [ ] Validar entrada JSON antes de procesar
- [ ] Manejar errores de API con mensajes claros al usuario
- [ ] Implementar logging estructurado para debugging
- [ ] No fallar completamente si un candidato falla (continuar con los demás)
- [ ] Mostrar resumen de errores al finalizar procesamiento

---

### RT-005: Performance
**Prioridad:** Media  
**Descripción:** El sistema debe procesar candidatos de forma eficiente.

**Criterios de Aceptación:**
- [ ] Procesar candidatos de forma secuencial (evitar rate limits)
- [ ] Implementar caché de respuestas LLM para inputs idénticos
- [ ] Mostrar progreso en tiempo real durante procesamiento
- [ ] Tiempo máximo total para 50 candidatos: 15 minutos
- [ ] Optimizar uso de memoria para grandes volúmenes

---

## 3. Requerimientos de Interfaz de Usuario

### UI-001: Vista de Carga de Archivos
**Prioridad:** Alta  
**Descripción:** Primera vista de carga - Interfaz para cargar archivos (PDF o JSON) mediante drag-and-drop o selector de archivos.

**Criterios de Aceptación:**
- [ ] Área de drag-and-drop para cargar múltiples archivos (PDF o JSON)
- [ ] Botón de selección de archivos para resumes (soporta PDF y JSON)
- [ ] Botón de selección de archivo para Job Description (soporta PDF y JSON)
- [ ] Mostrar preview de archivos cargados con información:
  - Nombre del archivo
  - Tipo (PDF o JSON)
  - Tamaño
  - Para PDFs: número de páginas
  - Estado de validación
- [ ] Validar archivos antes de habilitar botón de procesar
- [ ] Mostrar contador de resumes cargados (separado por tipo: PDF/JSON)
- [ ] Mostrar progreso de extracción de texto durante el procesamiento (solo para PDFs)
- [ ] Opción para eliminar archivos de la lista antes de procesar
- [ ] Indicador visual diferenciado para PDFs vs JSONs
- [ ] Botón "Buscar en Storage" para acceder a JSONs almacenados

---

### UI-002: Vista de Carga Tipo Formulario
**Prioridad:** Alta  
**Descripción:** Segunda vista de carga - Formulario estructurado para ingresar datos manualmente o desde storage.

**Criterios de Aceptación:**
- [ ] Formulario estructurado para ingresar datos de resume:
  - Campo de nombre
  - Campo de habilidades (multi-select o tags)
  - Sección de experiencia (agregar múltiples experiencias)
  - Sección de educación (agregar múltiples educaciones)
  - Campo de texto libre para información adicional
- [ ] Formulario estructurado para Job Description:
  - Campo de título del puesto
  - Campo de descripción
  - Lista de requisitos obligatorios (must-have)
  - Lista de requisitos deseables (nice-to-have)
  - Campo de años de experiencia requeridos
- [ ] Botón "Cargar desde Storage" para buscar y seleccionar JSONs previamente almacenados
- [ ] Modal o panel de búsqueda de storage con:
  - Lista de resumes JSON disponibles
  - Lista de job descriptions JSON disponibles
  - Filtros de búsqueda (por nombre, fecha, etc.)
  - Vista previa del JSON antes de seleccionar
- [ ] Validación de campos del formulario en tiempo real
- [ ] Opción de guardar formulario como borrador
- [ ] Botón para convertir formulario a JSON antes de procesar
- [ ] Botón para guardar JSON en storage después de completar formulario

---

### UI-003: Interfaz de Procesamiento
**Prioridad:** Alta  
**Descripción:** La interfaz debe mostrar el progreso del análisis.

**Criterios de Aceptación:**
- [ ] Barra de progreso mostrando candidatos procesados
- [ ] Contador: "Procesando candidato X de Y"
- [ ] Indicador de estado (procesando, completado, error)
- [ ] Botón para cancelar procesamiento (opcional)
- [ ] Mostrar tiempo estimado restante

---

### UI-004: Tabla de Resultados
**Prioridad:** Alta  
**Descripción:** La tabla debe mostrar resultados de forma clara y ordenada.

**Criterios de Aceptación:**
- [ ] Tabla responsive que se adapta a diferentes tamaños de pantalla
- [ ] Colores diferenciados por score (verde >80, amarillo 60-80, rojo <60)
- [ ] Columnas ordenables haciendo click en header
- [ ] Paginación si hay muchos resultados (10-20 por página)
- [ ] Búsqueda/filtro por nombre o score
- [ ] Expandir reason codes al hacer click en fila

---

### UI-005: Detalles de Candidato
**Prioridad:** Media  
**Descripción:** Mostrar detalles expandidos de cada candidato.

**Criterios de Aceptación:**
- [ ] Modal o panel lateral con detalles completos
- [ ] Mostrar resume completo parseado
- [ ] Resaltar secciones que coinciden con JD
- [ ] Mostrar reason codes con explicaciones detalladas
- [ ] Botón para cerrar/colapsar detalles

---

### UI-006: Exportación
**Prioridad:** Media  
**Descripción:** Botón y feedback de exportación.

**Criterios de Aceptación:**
- [ ] Botón "Exportar a CSV" visible y accesible
- [ ] Mostrar mensaje de éxito al exportar
- [ ] Mostrar ruta del archivo exportado
- [ ] Botón para descargar directamente (si aplica)

---

## 4. Requerimientos de Datos

### RD-001: Formato de Entrada
**Prioridad:** Alta  
**Descripción:** Definir estructura exacta de datos de entrada.

**Criterios de Aceptación:**
- [ ] Soportar archivos PDF como formato de entrada
- [ ] Soportar archivos JSON como formato de entrada
- [ ] Documentar estructura JSON completa para resumes
- [ ] Documentar estructura JSON completa para Job Description
- [ ] Proporcionar ejemplos de archivos PDF válidos
- [ ] Proporcionar ejemplos de archivos JSON válidos
- [ ] Validar que PDFs sean legibles antes de procesar
- [ ] Validar estructura JSON antes de procesar
- [ ] Validar estructura JSON generada después de conversión de PDF

---

### RD-002: Formato de Salida
**Prioridad:** Alta  
**Descripción:** Definir estructura exacta de datos de salida.

**Criterios de Aceptación:**
- [ ] CSV con columnas: rank, candidate_id, name, overall_score, similarity_score, must_have_hits, recency_boost, reason_codes, matched_requirements
- [ ] Reason codes en formato legible (separados por punto y coma)
- [ ] Scores como números decimales con 2 decimales
- [ ] Encoding UTF-8

---

## 5. Requerimientos de Configuración

### RC-001: Variables de Entorno
**Prioridad:** Alta  
**Descripción:** Configuración mediante variables de entorno.

**Criterios de Aceptación:**
- [ ] Archivo `.env` con todas las configuraciones necesarias
- [ ] `.env.example` como template
- [ ] Validar que API key esté configurada antes de ejecutar
- [ ] Documentar todas las variables en README

**Variables Requeridas:**
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `LLM_TEMPERATURE`
- `SIMILARITY_WEIGHT`
- `MUST_HAVE_BOOST_WEIGHT`
- `RECENCY_BOOST_WEIGHT`

**Variables de Storage:**
- `STORAGE_TYPE`: local, s3, azure, gcs
- `STORAGE_PATH`: Ruta local o configuración de cloud storage
- `AWS_ACCESS_KEY_ID`: Para AWS S3 (si aplica)
- `AWS_SECRET_ACCESS_KEY`: Para AWS S3 (si aplica)
- `AWS_S3_BUCKET`: Nombre del bucket S3 (si aplica)
- `AZURE_STORAGE_CONNECTION_STRING`: Para Azure Blob (si aplica)
- `AZURE_STORAGE_CONTAINER`: Nombre del container (si aplica)
- `GCS_PROJECT_ID`: Para Google Cloud Storage (si aplica)
- `GCS_BUCKET_NAME`: Nombre del bucket GCS (si aplica)

---

## 6. Requerimientos de Testing

### TEST-001: Tests Unitarios
**Prioridad:** Media  
**Descripción:** Implementar tests para componentes individuales.

**Criterios de Aceptación:**
- [ ] Tests para `pdf_extractor.py` (extracción de texto de PDFs)
- [ ] Tests para `resume_parser.py` (parsing de texto a JSON)
- [ ] Tests para `jd_parser.py` (parsing de JD a JSON)
- [ ] Tests para `hybrid_scorer.py`
- [ ] Tests para `csv_exporter.py`
- [ ] Cobertura mínima: 70%

---

### TEST-002: Tests de Integración
**Prioridad:** Media  
**Descripción:** Tests end-to-end del flujo completo.

**Criterios de Aceptación:**
- [ ] Test completo con 3-5 resumes de ejemplo
- [ ] Validar formato de salida CSV
- [ ] Validar que scores estén en rango correcto
- [ ] Validar que reason codes se generen correctamente

---

## 7. Criterios de Aceptación Globales

### CAG-001: Demo Funcional
**Prioridad:** Alta  
**Descripción:** El sistema debe funcionar end-to-end para la demo.

**Criterios de Aceptación:**
- [ ] Cargar al menos 5 resumes en formato PDF desde vista de carga
- [ ] Cargar al menos 5 resumes en formato JSON desde vista de carga
- [ ] Cargar 1 Job Description desde vista de carga (PDF o JSON)
- [ ] Cargar 1 resume desde vista de formulario
- [ ] Buscar y cargar al menos 1 JSON desde storage
- [ ] Extraer texto de todos los PDFs exitosamente
- [ ] Convertir texto extraído a JSON estructurado
- [ ] Guardar JSONs procesados en storage
- [ ] Procesar todos los candidatos sin errores críticos
- [ ] Mostrar tabla rankeada con resultados
- [ ] Exportar resultados a CSV exitosamente
- [ ] Tiempo total de procesamiento (Carga → JSON → Análisis) < 15 minutos para 10 candidatos

---

### CAG-002: Documentación
**Prioridad:** Media  
**Descripción:** Documentación suficiente para usar el sistema.

**Criterios de Aceptación:**
- [ ] README.md con instrucciones de instalación
- [ ] README.md con instrucciones de uso
- [ ] Documentar estructura de datos de entrada
- [ ] Documentar formato de salida
- [ ] Incluir ejemplos de uso

---

## Notas de Implementación

### Consideraciones Especiales
- La maquetación ya está disponible, los requerimientos UI deben adaptarse a lo existente
- Priorizar funcionalidad sobre perfección estética en esta fase
- Los prompts son críticos para la calidad del análisis - iterar según resultados
- Considerar costos de API al procesar grandes volúmenes

### Próximos Pasos
1. Revisar y ajustar requerimientos según feedback
2. Priorizar requerimientos marcados como "Alta"
3. Crear historias de usuario (user stories) para desarrollo ágil
4. Definir criterios de aceptación más detallados para cada requerimiento

