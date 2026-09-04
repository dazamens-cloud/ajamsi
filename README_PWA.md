# 🚀 AJAMSI - Control Panel PWA

**Sistema de generación automática de contenido para TikTok/Instagram con pipeline de 4 fases**

---

## 🎯 Características

- ✅ **Fase 1**: Scraping real de noticias de Canarias (RSS + BeautifulSoup)
- ✅ **Fase 2**: Generación de ideas y prompts visuales con Ollama (IA local)
- ✅ **Fase 3**: Generación automática de captions/títulos
- ✅ **Fase 4**: Compilación de videos en 3 formatos (TikTok, Instagram, YouTube) con FFmpeg
- 🎨 **Interfaz web moderna**: Dark mode, wizard-style, estado en tiempo real
- 💰 **Costo $0/mes**: Ollama local + FFmpeg (sin APIs de pago)

---

## 📋 Requisitos Previos

### 1. **Python 3.12+**
```bash
python --version
```

### 2. **Ollama instalado y ejecutándose**
```bash
ollama serve
# En otra terminal/ventana, verifica que se está ejecutando en http://localhost:11434
```

### 3. **FFmpeg instalado**
```bash
ffmpeg -version
```

### 4. **Imagen de ejemplo** (para Fase 4)
- Coloca una imagen en: `imagenes/el_tipico_canario.png`
- O cualquier otra imagen que uses como base para los videos

---

## 🚀 Instalación Rápida

### Opción A: Script `.bat` (Windows - RECOMENDADO)
```bash
# Simplemente haz doble click en:
run_pwa.bat

# Se abrirá automáticamente el navegador en http://localhost:5000
```

### Opción B: PowerShell
```powershell
.\run_pwa.ps1
```

### Opción C: Manual
```bash
# Instalar dependencias
pip install -r requirements_pwa.txt

# Ejecutar servidor
python app_backend.py

# En otro navegador, abre:
# http://localhost:5000
```

---

## 🎮 Cómo Usar

### 1️⃣ **Inicializar el Sistema**
Haz clic en **"Iniciar Sistema"** → Se cargan los 10 agentes

### 2️⃣ **Fase 1: Scraping Real**
Haz clic en **"🕷️ Iniciar"** → El sistema descarga ~12 noticias de:
- 📰 Diario de Avisos
- 📰 Canarias Ahora
- Y más fuentes RSS de Canarias

Aparecerán como **tarjetas grandes** donde puedes seleccionar una noticia.

### 3️⃣ **Fase 2: Ideas + Prompts**
Después de seleccionar una noticia → Haz clic en **"💡 Iniciar"**
- Genera 2 ideas creativas basadas en la noticia
- Crea prompts visuales con estilos: folclórico, cartoon, vintage, etc.
- Usa **Ollama (IA local)** para una mejor calidad

### 4️⃣ **Fase 3: Captions**
Haz clic en **"✍️ Iniciar"**
- Genera 3 títulos/captions optimizados para redes sociales
- Incluye hashtags y emojis

### 5️⃣ **Fase 4: Compilar Video**
Haz clic en **"🎬 Iniciar"**
- FFmpeg compila un video MP4 con la imagen, captions y música de fondo
- Soporta 3 resoluciones:
  - **TikTok**: 1080x1920 (vertical)
  - **Instagram**: 1080x1080 (cuadrado)
  - **YouTube**: 1920x1080 (horizontal)
- Archivo generado: `video_YYYYMMDD_HHMMSS_[formato].mp4`

### ✅ **Reset**
Haz clic en **"🔄 Resetear"** para volver a empezar desde Fase 1

---

## 📊 Arquitectura Técnica

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (React + Tailwind CSS)                        │
│  app_frontend.html → http://localhost:5000/             │
└──────────────────────┬──────────────────────────────────┘
                       │ /api/state (polling cada 1s)
┌──────────────────────▼──────────────────────────────────┐
│  Backend API (Flask)                                    │
│  app_backend.py → http://localhost:5000/api/            │
├──────────────────────────────────────────────────────────┤
│ Endpoints:                                               │
│  - POST /api/init          → Inicializa AgentOrchestrator
│  - POST /api/phase1        → Scraping RSS               │
│  - POST /api/phase2        → Ideas + Ollama Prompts     │
│  - POST /api/phase3        → Captions                   │
│  - POST /api/phase4        → Video FFmpeg               │
│  - GET  /api/state         → Estado en tiempo real      │
│  - POST /api/reset         → Reiniciar pipeline         │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┬───────────────┐
        │              │              │               │
   ┌────▼──────┐ ┌────▼──────┐ ┌────▼──────┐ ┌──────▼────┐
   │ScraperAgent│ │OllamaAgent│ │CaptionAgent│ │VideoAgent │
   │(RSS+BS4)   │ │(localhost)│ │(template) │ │(FFmpeg)   │
   └────────────┘ └───────────┘ └───────────┘ └───────────┘
```

---

## 🔧 Configuración

### `config/config.json`
```json
{
  "prompt_engineer": {
    "model": "qwen3.5:9b",
    "url": "http://localhost:11434",
    "timeout": 30
  }
}
```

### Cambiar modelo Ollama
Si quieres usar otro modelo (ej: `mistral`, `neural-chat`):

1. **Descarga el modelo**:
   ```bash
   ollama pull mistral
   ```

2. **Edita `config/config.json`**:
   ```json
   "model": "mistral"
   ```

---

## 📁 Estructura de Archivos

```
ajamsi/
├── app_backend.py              # Servidor Flask
├── app_frontend.html            # Interfaz React
├── run_pwa.bat                 # Script Windows (doble click)
├── run_pwa.ps1                 # Script PowerShell
├── requirements_pwa.txt         # Dependencias
├── config/
│   └── config.json             # Configuración
├── src/
│   ├── agent_orchestrator.py   # Orquestador de 10 agentes
│   ├── agents/
│   │   ├── scraper_agent.py    # RSS + BeautifulSoup
│   │   ├── ollama_prompt_engineer_agent.py
│   │   ├── caption_generator_agent.py
│   │   └── video_compiler_agent.py
│   └── utils/
│       └── config_loader.py
├── imagenes/
│   └── el_tipico_canario.png   # Imagen base (o la tuya)
├── videos/                      # Donde se guardan videos
└── README_PWA.md               # Este archivo
```

---

## 🐛 Troubleshooting

### ❌ "Error: Ollama no disponible"
```
✓ Verifica que ejecutaste: ollama serve
✓ En otra terminal, prueba: curl http://localhost:11434
✓ Si no responde, reinicia: ollama serve
```

### ❌ "Error: FFmpeg no encontrado"
```
✓ En Windows: descarga ffmpeg de https://ffmpeg.org/download.html
✓ En Mac: brew install ffmpeg
✓ En Linux: apt-get install ffmpeg
✓ Verifica: ffmpeg -version
```

### ❌ "Puerto 5000 ya en uso"
```
✓ Busca qué proceso usa el puerto:
  Windows: netstat -ano | findstr :5000
✓ Cierra la aplicación o cambia el puerto en app_backend.py:
  app.run(debug=True, port=5001)  # Cambia a 5001
```

### ❌ "No se genera video, solo espera"
```
✓ FFmpeg es lento en Windows (especialmente H.264)
✓ Espera 2-5 minutos en la primera ejecución
✓ Si no termina en 10 minutos:
  - Verifica que FFmpeg esté instalado
  - Revisa que la imagen exista: imagenes/el_tipico_canario.png
  - Mira los logs en la consola de app_backend.py
```

### ❌ "CORS error en el navegador"
```
✓ Ya debería estar configurado con flask-cors
✓ Si persiste, verifica que app_backend.py tenga:
  from flask_cors import CORS
  CORS(app)
```

---

## 📚 APIs Backend

### GET `/api/state`
Obtiene el estado actual del sistema en tiempo real.

**Respuesta:**
```json
{
  "status": "loading|ready|error|idle",
  "current_phase": 0,
  "noticias": [
    {
      "titulo": "Noticia...",
      "fuente": "Diario de Avisos",
      "relevancia_score": 85.5
    }
  ],
  "ideas": [{ "titulo": "Idea..." }],
  "prompts": [{ "estilo": "folclórico", "prompt_text": "..." }],
  "captions": [{ "caption": "Caption..." }],
  "video": {
    "video_filename": "video_20260903_120000_tiktok.mp4",
    "tamaño_mb": 12.5,
    "resolucion": "1080x1920"
  },
  "error": null,
  "timestamp": "2026-09-03T12:00:00"
}
```

### POST `/api/init`
Inicializa el orquestador con 10 agentes.

### POST `/api/phase1`
Ejecuta Fase 1: Scraping de noticias.

### POST `/api/phase2`
Ejecuta Fase 2: Ideas + Prompts.

**Body:**
```json
{
  "noticia_idx": 0
}
```

### POST `/api/phase3`
Ejecuta Fase 3: Captions.

### POST `/api/phase4`
Ejecuta Fase 4: Video.

### POST `/api/reset`
Reinicia el pipeline.

---

## 🎓 Ejemplos de Uso

### Ejecutar Completo en Bash (para testing)
```bash
#!/bin/bash

# 1. Inicializar
curl -X GET http://localhost:5000/api/init

# 2. Esperar estado ready
sleep 3

# 3. Fase 1
curl -X POST http://localhost:5000/api/phase1

# 4. Esperar
sleep 5

# 5. Fase 2
curl -X POST http://localhost:5000/api/phase2 \
  -H "Content-Type: application/json" \
  -d '{"noticia_idx": 0}'

# 6. Fase 3
curl -X POST http://localhost:5000/api/phase3

# 7. Fase 4
curl -X POST http://localhost:5000/api/phase4

# 8. Ver estado final
curl -X GET http://localhost:5000/api/state | jq .
```

---

## 💡 Próximos Pasos

- [ ] Agregar autenticación OAuth para Google Drive
- [ ] Implementar caché de noticias para evitar duplicados
- [ ] Soporte para múltiples idiomas (Inglés, Francés)
- [ ] Dashboard de analytics (noticias más populares, etc.)
- [ ] Publicación automática a TikTok/Instagram API
- [ ] Presets personalizados para diferentes estilos de contenido

---

## 📞 Soporte

Si tienes problemas:

1. **Revisa los logs** en la consola donde ejecutaste `app_backend.py`
2. **Abre el navegador** en las DevTools (F12) → Console tab
3. **Verifica los requisiots**: Ollama, FFmpeg, Python 3.12+

---

**Hecho con ❤️ usando Claude AI + Ollama + FFmpeg**
