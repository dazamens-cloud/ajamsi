# 🎬 AjamSi - Sistema Automático de Generación de Contenido TikTok

> **Estado:** FASE 0 - Setup Inicial ✅  
> **Versión:** 0.1.0  
> **Última actualización:** 2026-08-27

## 📋 Descripción

**AjamSi** es un sistema automático que convierte noticias de Canarias/Lanzarote en contenido humorístico para TikTok.

### 🎯 Objetivo Principal

Automatizar la generación de contenido para la cuenta [@hummorkana](https://www.tiktok.com/@hummorkana) usando:
- ✅ Web scraping de noticias locales
- ✅ Generación de ideas con Claude
- ✅ Generación de imágenes con Gemini Plus
- ✅ Compilación automática de videos
- ✅ Sistema de aprendizaje basado en feedback

## 🏗️ Estructura del Proyecto

```
ajamsi/
├── src/
│   ├── scrapers/          # Web scraping de noticias
│   ├── generators/        # Generadores de ideas e imágenes
│   ├── processors/        # Compiladores de videos
│   ├── utils/             # Utilidades (DB, config, etc.)
│   ├── constants.py       # Constantes del proyecto
│   └── __init__.py
├── data/
│   ├── raw/               # Noticias sin procesar
│   ├── processed/         # Noticias procesadas
│   ├── images/            # Imágenes generadas
│   ├── videos/            # Videos compilados
│   ├── ajamsi.db          # Base de datos SQLite
│   └── preferences.json   # Base de aprendizaje
├── config/
│   └── config.json        # Configuración del proyecto
├── tests/                 # Tests unitarios
├── logs/                  # Logs de ejecución
├── output/                # Archivos de salida
├── main.py                # Script principal
├── requirements.txt       # Dependencias Python
└── README.md              # Este archivo
```

## 🚀 Instalación y Setup

### 1. Prerrequisitos

- Python 3.10+
- Git
- FFmpeg (para compilación de videos)
- Gemini Plus (suscripción activa)
- Google Drive API (configurada)

### 2. Instalación

```bash
# Clonar o navegar al proyecto
cd ajamsi

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración

#### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Gemini API
GEMINI_API_KEY=tu_api_key_aqui

# Google Drive
GOOGLE_DRIVE_CREDENTIALS=path/to/credentials.json

# Claude API (para generador de ideas)
CLAUDE_API_KEY=tu_api_key_aqui

# Logging
LOG_LEVEL=INFO
```

#### Archivos de Configuración

- `config/config.json` - Configuración principal del sistema
- `data/preferences.json` - Base de aprendizaje y preferencias

## 📊 Workflow

### Procesamiento por Bloques

```
SESIÓN TÍPICA:

1. BLOQUE SCRAPING
   → Bot scrappea noticias (últimos 7 días)
   → Guarda en DB local
   → Muestra top 7 noticias

2. BLOQUE IDEAS
   → Genera 2-3 conceptos de meme por noticia
   → Estilo: "El Típico" canario
   → Humor: Sardónico, local

3. BLOQUE IMÁGENES
   → Genera prompts optimizados
   → Llama Gemini Plus API
   → Descarga 7 imágenes

4. BLOQUE GUIONES
   → Genera captions + hashtags
   → Máx 280 caracteres
   → Trending local

5. BLOQUE VIDEOS
   → Compila imagen + audio + efectos (FFmpeg)
   → Genera 7 videos MP4
   → Sube a Google Drive

6. BLOQUE FEEDBACK
   → Usuario: "videos 1, 4, 7 → ✅, resto → ❌"
   → Sistema actualiza preferences.json
   → Próximo batch = mejorado
```

## 🔄 Fases de Escalamiento

| Fase | Cuándo | Qué hace Claude | Qué haces tú |
|------|--------|-----------------|-------------|
| **1: Interactivo** | Ahora (videos 1-20) | Genera bajo tu dirección | Das ideas, apruebas cada paso |
| **2: Semi-auto** | 20+ videos | Genera ideas automáticas | Validas imagen y guión |
| **3: Automático** | 50+ videos | Batch completo sin supervisión | Solo checas antes de subir |

## 📰 Fuentes de Noticias

### Prioridad 1 (Lanzarote)
- [Lancelot Digital](https://www.lancelotdigital.com/lanzarote)
- [Crónicas de Lanzarote](https://www.cronicasdelanzarote.es/)
- [Noticias de Lanzarote](https://www.noticiasdelanzarote.com/)
- [Diario de Lanzarote](https://www.diariodelanzarote.com/)
- [El Periódico de Lanzarote](https://www.elperiodicodelanzarote.com/)

### Prioridad 2 (Canarias)
- [Canarias Ahora](https://www.eldiario.es/canariasahora/)

## 🛠️ Tecnología

| Componente | Herramienta | Descripción |
|-----------|-----------|-------------|
| Web Scraping | BeautifulSoup + Python | Extrae noticias de sitios web |
| Generación de Imágenes | Gemini Plus API | Crea ilustraciones |
| Generación de Ideas | Claude API | Crea conceptos de memes |
| Compilación de Video | FFmpeg + Python | Edita y compila videos |
| Base de Datos | SQLite | Almacena noticias, ideas, videos |
| Sync Automático | Google Drive SDK | Backup automático |

## 📚 Módulos Principales

### `src/utils/db.py`
Gestor de base de datos SQLite con tablas para:
- Noticias
- Ideas generadas
- Imágenes
- Videos compilados
- Feedback del usuario

### `src/utils/config_loader.py`
Cargador de configuración JSON con métodos de acceso por puntos

### `src/constants.py`
Constantes del proyecto, rutas, valores por defecto

## 🎮 Uso

### Ejecutar interfaz interactiva

```bash
python main.py
```

Esto abrirá un menú interactivo donde puedes:
1. Scrapear noticias
2. Generar ideas
3. Generar imágenes
4. Compilar videos
5. Ver estadísticas
6. Configurar preferencias

## 📊 Base de Datos

### Esquema

#### Tabla: `noticias`
- id, titulo, url, fuente, contenido, fecha_publicacion, fecha_scrapeado, relevancia_score, usado

#### Tabla: `ideas`
- id, noticia_id, concepto, angulo_humor, estado, fecha_creacion, feedback

#### Tabla: `imagenes`
- id, idea_id, ruta_archivo, prompt_usado, proveedor, fecha_generacion, estado

#### Tabla: `videos`
- id, imagen_id, idea_id, ruta_archivo, guion, duracion_segundos, estado, subido_tiktok

#### Tabla: `feedback_log`
- id, video_id, idea_id, imagen_id, tipo_feedback, comentario, fecha

## 🎓 Sistema de Aprendizaje

El archivo `data/preferences.json` mantiene:
- Temas que funcionan bien
- Estilos efectivos
- Prompts que generan buenos resultados
- Métricas de éxito
- Historial de feedback

Se actualiza automáticamente basándose en el feedback del usuario.

## 📋 Próximos Pasos (FASE 1)

- [ ] Implementar web scraper funcional
- [ ] Integración Gemini Plus API
- [ ] Generador de ideas con Claude
- [ ] Compilador de videos FFmpeg
- [ ] Sistema de sync a Google Drive
- [ ] Tests unitarios

## 🤝 Contribuir

Este es un proyecto personal. Para cambios, ajusta directamente los archivos o pide feedback.

## 📄 Licencia

Proyecto personal - No aplicable

## 👤 Autor

- **Andrés** (@hummorkana)
- **AI Assistant:** Claude

---

**Última actualización:** 2026-08-27  
**Estado:** En desarrollo activo 🔧
