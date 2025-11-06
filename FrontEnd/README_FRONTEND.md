# 🎨 AI Talent Matcher - Frontend

Frontend de la aplicación AI Talent Matcher construido con React, TypeScript, Material-UI y Vite.

## 🚀 Características

- **File Upload**: Sube resumes (PDF/JSON) y job descriptions
- **Manual Entry**: Ingresa datos manualmente mediante formularios
- **Real-time Processing**: Monitorea el progreso del análisis en tiempo real
- **Results Dashboard**: Visualiza candidatos rankeados con scores detallados
- **Job Descriptions View**: Explora todas las JDs y ve candidatos rankeados por posición

## 🛠️ Stack Tecnológico

- **Framework**: React 18 con TypeScript
- **UI Library**: Material-UI (MUI) v6
- **Build Tool**: Vite
- **State Management**: TanStack Query (React Query)
- **Routing**: React Router v6
- **Styling**: Emotion + Tailwind CSS
- **HTTP Client**: Ky

## 📋 Requisitos Previos

- **Node.js**: 18.x o superior
- **npm**: 9.x o superior
- **Backend**: El backend debe estar corriendo en `http://localhost:8000`

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias

```bash
cd FrontEnd
npm install
```

### 2. Configurar Variables de Entorno

El archivo `.env.local` ya está configurado para desarrollo:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Iniciar Servidor de Desarrollo

```bash
npm run dev
```

La aplicación se abrirá automáticamente en `http://localhost:3000`

## 📜 Scripts Disponibles

```bash
# Desarrollo
npm run dev              # Inicia servidor de desarrollo

# Build
npm run build            # Genera build de producción
npm run preview          # Preview del build de producción

# Linting
npm run lint             # Ejecuta ESLint
npm run lint:fix         # Ejecuta ESLint y corrige errores

# Type Checking
npm run type-check       # Verifica tipos de TypeScript
```

## 🏗️ Estructura del Proyecto

```
FrontEnd/
├── src/
│   ├── app/
│   │   └── (control-panel)/
│   │       └── apps/
│   │           └── talent-matcher/
│   │               ├── api/               # API services y hooks
│   │               │   ├── hooks/        # React Query hooks
│   │               │   ├── services/     # API calls (analysisApi, storageApi)
│   │               │   └── types/        # TypeScript types
│   │               ├── components/
│   │               │   ├── forms/        # Formularios
│   │               │   ├── ui/           # Componentes UI
│   │               │   └── views/        # Vistas principales
│   │               │       ├── TalentMatcherAppView.tsx   # Vista principal
│   │               │       ├── FileUploadView.tsx         # Upload de archivos
│   │               │       ├── FormView.tsx               # Entrada manual
│   │               │       ├── ProcessingView.tsx         # Monitoreo de proceso
│   │               │       ├── ResultsView.tsx            # Resultados
│   │               │       └── JobDescriptionsView.tsx    # Lista de JDs
│   │               └── route.tsx         # Configuración de ruta
│   ├── utils/
│   │   └── api.ts                        # Cliente HTTP configurado
│   └── ...
├── vite.config.mts                       # Configuración de Vite
└── package.json
```

## 🔌 Integración con Backend

El frontend se comunica con el backend a través de un proxy configurado en Vite:

```typescript
// vite.config.mts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

### Endpoints Principales

- `POST /api/upload/resumes` - Subir resumes
- `POST /api/upload/job-description` - Subir job description
- `POST /api/process` - Iniciar procesamiento
- `GET /api/process/status` - Obtener estado del procesamiento
- `GET /api/results` - Obtener resultados rankeados
- `GET /api/storage/resumes` - Listar resumes almacenados
- `GET /api/storage/job-descriptions` - Listar JDs almacenadas

## 🎯 Flujo de Uso

### 1. Nueva Análisis

1. Ir a la pestaña **"New Analysis"**
2. Elegir entre:
   - **File Upload**: Subir archivos PDF o JSON
   - **Manual Entry**: Ingresar datos mediante formulario
3. Subir resumes y job description
4. Hacer click en **"Start Analysis"**
5. Monitorear el progreso en tiempo real
6. Ver resultados rankeados

### 2. Ver Job Descriptions y Candidatos

1. Ir a la pestaña **"Job Descriptions & Results"**
2. Ver lista de todas las Job Descriptions disponibles
3. Hacer click en una JD para ver:
   - Detalles de la posición
   - Requirements (Must-Have y Nice-to-Have)
   - Candidatos rankeados con scores detallados
   - Reason codes y matched requirements

## 🎨 Características de UI

### Componentes Principales

**TalentMatcherAppView**
- Navegación principal con tabs
- Gestión de estado de la aplicación

**FileUploadView**
- Drag & drop de archivos
- Preview de archivos subidos
- Validación de formato (PDF/JSON)

**JobDescriptionsView** (Nueva)
- Grid de tarjetas de JDs
- Vista detallada de candidatos rankeados
- Scores visuales con colores
- Badges para top 3 candidatos
- Reason codes y requirements matched

**ProcessingView**
- Progress bar con porcentaje
- Tiempo estimado restante
- Estado en tiempo real

**ResultsView**
- Tabla de candidatos rankeados
- Scores detallados
- Export a CSV

## 🐛 Troubleshooting

### El frontend no se conecta al backend

1. Verificar que el backend esté corriendo:
   ```bash
   # En el directorio raíz del proyecto
   python run_server.py
   ```

2. Verificar la URL del backend en `.env.local`:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

3. Verificar el proxy en `vite.config.mts`

### Errores de CORS

Si ves errores de CORS, verifica que el backend tenga CORS habilitado:

```python
# src/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Build falla

1. Limpiar cache y node_modules:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

2. Limpiar build:
   ```bash
   rm -rf build
   npm run build
   ```

## 📦 Build de Producción

```bash
# Generar build
npm run build

# Preview del build
npm run preview
```

El build se genera en el directorio `build/`.

## 🔧 Configuración Avanzada

### Cambiar Puerto

Editar `vite.config.mts`:

```typescript
server: {
  port: 3001  // Cambiar aquí
}
```

### Configurar API Backend

Para producción, actualizar `.env`:

```env
VITE_API_BASE_URL=https://api.tudominio.com
```

## 📝 Notas de Desarrollo

- El frontend usa **MSW (Mock Service Worker)** en modo desarrollo para testing
- Los tipos TypeScript están sincronizados con el backend
- React Query maneja caching y refetching automático
- Material-UI v6 con theming personalizable

## 🤝 Contribuir

1. Crear una rama para tu feature
2. Hacer commits descriptivos
3. Asegurar que no hay errores de linting: `npm run lint`
4. Hacer pull request

---

**Desarrollado para el Hackatón Equipo E** 🚀
