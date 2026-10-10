# 🎬 AJAMSI Dashboard — Monitor en Tiempo Real

Sistema completo para generar contenido de TikTok a partir de noticias de Canarias. **100% local, $0/mes.**

## 🚀 Inicio Rápido

```bash
cd D:\proyectos godot\tik tok\ajamsi
.\lanzar.bat
```

Se abrirá automáticamente: **http://localhost:5000** (Dashboard)

## 📊 Dos Interfaces

### 1. **Dashboard** (http://localhost:5000) ← COMIENZA AQUÍ
- Monitor en tiempo real del pipeline
- Estadísticas de producción
- Logs en vivo (últimas 50 líneas)
- Botones de control

**Funciones:**
- ▶️ Iniciar Pipeline
- 📷 Modo: Solo Imágenes (recomendado) o Imágenes + Videos
- 📂 Abrir carpeta /videos/
- 🔄 Reiniciar sistema

### 2. **Studio** (http://localhost:5000/studio)
- PWA completa para editar detalles
- Selector de noticias
- Ajustes de captions
- Composer de imagen meme

---

## 🎯 ¿Qué Hace AJAMSI?

```
Noticias RSS (Canarias)
        ↓
    📰 Scraping
        ↓
    💡 Ideas (humor canario)
        ↓
    ✍️ Captions (descripciones)
        ↓
    🖼️ Imagen (tarjeta meme 1080x1920)
        ↓
    📄 Documento Word (guion + hashtags)
        ↓
    🎬 Video (opcional, con Ken Burns)
        ↓
    /videos/ (carpeta con todo listo)
```

## 📁 Estructura de Salida

```
/videos/
├── GUIA_PUBLICACION_20260922_134521.docx   ← Copiar aquí captions y hashtags
├── vineta_20260922_134500_000123.png       ← Imágenes para subir a TikTok
├── vineta_20260922_134501_000456.png
├── noticia1_video_20260922_134502_tiktok.mp4  ← Videos (si modo=video)
└── noticia2_video_20260922_134503_tiktok.mp4
```

## 🎨 Características

### Imagen Generada (1080x1920)
- Fondo: cielo canario degradado + arena
- Personaje: "El Típico Canario" (PNG transparente)
- Setup: "CHACHO, NUEVA NOTICIA..." (blanco con contorno)
- Remate: Hook canario (amarillo) — p.ej. "MÁS FELIZ QUE TURISTA EN EL TEIDE"
- Contexto: titular pequeño de la noticia

### Documento Word
- **Guion**: texto para agregar voz en TikTok Studio
- **Captions**: 3 variantes, scored por engagement
- **Hashtags**: optimizados por plataforma (#TikTok, #Reels, #Shorts)
- **Consejos**: hora de publicación, estrategia de hashtags

### Modos

| Modo | Salida | Tiempo | Caso de Uso |
|------|--------|--------|-----------|
| **Imágenes** | PNG | ~5-10 seg/imagen | ⭐ Recomendado: TikTok Studio con tus efectos |
| **Video** | MP4 + PNG | ~30-60 seg/video | Para publicar directo sin editar |

## 📊 Dashboard: ¿Qué Ves?

### Estado del Sistema
- 🔧 Estado del Sistema — Verificación de dependencias
- 📡 Conexión API — Conectividad con el servidor
- ⚙️ Pipeline — Si está activo o inactivo

### Estadísticas
- Noticias procesadas
- Imágenes generadas
- Videos generados
- Tiempo promedio

### Controles
1. **Selector de Modo** — "Solo Imágenes" (default) o "Imágenes + Videos"
2. **Barra de Progreso** — % en tiempo real
3. **Botones** — Iniciar, Detener, Abrir carpeta, Reiniciar

### Logs en Vivo
- Cada línea muestra: Hora | Nivel | Mensaje
- Colores: 🔵 INFO | 🟢 OK | 🔴 ERROR | 🟡 WARN
- Últimas 50 líneas guardadas

---

## 🔧 Tecnología

| Componente | Stack |
|---|---|
| **Backend** | Flask (Python) + threading |
| **Frontend** | HTML5 vanilla + CSS (tema oscuro) |
| **Orquestación** | 10 agentes Python |
| **Noticias** | RSS feeds + BeautifulSoup |
| **Imágenes** | PIL/Pillow |
| **Video** | FFmpeg (H.264 + AAC) |
| **Narración** | pyttsx3 (Windows SAPI) → texto, tú agregas voz |
| **Documento** | python-docx |
| **LLM** | Ollama (Qwen 3.5:9b) — local |

---

## 💰 Monetización

| Método | Plazo | Dinero |
|--------|-------|--------|
| Creator Fund | 2-3 meses | $50-500/mes |
| Sponsorships | 4+ meses | $500-2000/video |
| Patreon | Inmediato | Variable |

**Tu ventaja**: Generas 5-10 videos/día con 0 fricción → volumen alto → audiencia rápido.

---

## 🆘 Troubleshooting

### "Puerto 5000 en uso"
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "Error: Python no encontrado"
Edita `lanzar.bat` y actualiza `PYTHON_PATH` a tu ruta de Python.

### "Las imágenes tienen fondo negro"
Verificar que `el_tipico_canario_transparente.png` existe en `/imagenes/`

### "FFmpeg error"
Instalar: `choco install ffmpeg` o descargar desde https://ffmpeg.org/download.html

---

## 📈 Caso Real: $1000/mes

**Asunciones:**
- 7 posts/día = 210/mes
- 10% se viral (50K views) = 50 videos × 50K = 2.5M views
- Creator Fund: 0.02 USD / 1K views = $50
- Sponsorships: 10 videos × $1000 = $10K

**Realista (mes 6):**
- 200K views/mes = $4 Creator Fund
- 5 sponsorships = $2500
- **Total: ~$2500/mes**

---

## 📞 Próximos Pasos

- [ ] Publicar 30 días seguidos (construir audiencia)
- [ ] Analizar cuál tipo de noticia da más engagement
- [ ] Contactar marcas canarias para sponsorships
- [ ] (Opcional) Auto-publicación con n8n (Fase 5)

---

**AJAMSI v1.0** | 2026-09-22 | `@hummorkana` style
