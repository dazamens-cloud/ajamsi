# 🔄 Workflow - Proceso de Generación

## Flujo General

```
INICIO
  ↓
BLOQUE SCRAPING (Noticias)
  ↓
BLOQUE IDEAS (Concepto)
  ↓
BLOQUE IMÁGENES (Gemini)
  ↓
BLOQUE GUIONES (Claude)
  ↓
BLOQUE VIDEOS (FFmpeg)
  ↓
BLOQUE FEEDBACK (Aprendizaje)
  ↓
ACTUALIZAR PREFERENCES.JSON
  ↓
FIN
```

## Procesamiento por BLOQUES

Se procesan **5-7 videos de una sesión completa**, no uno en uno.

### Ventajas del Procesamiento por Bloques

✅ **Eficiencia:** Generas todas las imágenes de una (no parar/continuar 7 veces)  
✅ **Feedback rápido:** Ves 5-7 videos juntos, feedback más rápido  
✅ **Aprendizaje:** Ves patrones acumulados  
✅ **Escalable:** Eventualmente sin supervisión  
✅ **Psicológico:** "Termino bloque = misión cumplida"

---

## Fase 1: Interactivo (AHORA - Videos 1-20)

### Rol del Usuario
- ✅ Das ideas/temas
- ✅ Apruebas/rechazas cada paso
- ✅ Das feedback
- ❌ No necesitas generar imágenes
- ❌ No necesitas compilar videos

### Rol del Sistema (Claude)
- ✅ Genera prompts optimizados
- ✅ Llama Gemini Plus
- ✅ Descargar imágenes
- ✅ Genera guiones
- ✅ Compila videos
- ✅ Aprende del feedback

### Sesión Típica

```
TÚ (en Cowork):
  "Vamos a generar semana"

CLAUDE (Sistema):
  
  1️⃣ BLOQUE SCRAPING
     → Busco noticias últimos 7 días
     → Te muestro top 7
     → "¿Cuál te llama?"
  
  2️⃣ BLOQUE IDEAS
     → Para cada noticia elegida
     → Genero 2-3 conceptos de meme
     → Estilo: El Típico canario
     → "¿Cuál opción A, B o C?"
  
  3️⃣ BLOQUE IMÁGENES
     → Genero prompts optimizados
     → Llamo Gemini Plus
     → Descargo imágenes
     → Te muestro galería
     → Tú: "la 3 y 5 no van, regenera"
  
  4️⃣ BLOQUE GUIONES
     → Leo imagen + contexto
     → Genero guión/captions
     → Máx 280 caracteres
     → Hashtags trending
     → "¿Aprobado?"
  
  5️⃣ BLOQUE VIDEOS
     → Compilo imagen + audio + transiciones
     → Genero 7 videos MP4
     → Subo a Google Drive
     → "Links listos para revisar"
  
  6️⃣ BLOQUE FEEDBACK & APRENDIZAJE
     → Tú: "videos 1, 4, 7 → ✅, resto → ❌"
     → Yo actualizo preferences.json
     → Próximo batch = mejorado
```

---

## Fase 2: Semi-Automático (Después 20+ Videos)

### Cambios
- Usuario solo **valida** imagen final (no elige)
- Sistema genera ideas automáticamente
- Usuario sigue dando feedback

### Flujo Fase 2
```
TÚ: "Generar semana"
CLAUDE: → Scraping → Ideas AUTO → Imágenes → Guiones → Videos
TÚ: "Revisar y dar feedback"
CLAUDE: "Actualizado, listo próximo batch"
```

---

## Fase 3: Automático (Después 50+ Videos)

### Cambios
- Sistema genera **todo** sin supervisión
- Usuario solo da **feedback ocasional**
- Mejora continua automática

### Flujo Fase 3
```
CLAUDE (Background):
  Cada semana:
    → Scraping automático
    → Ideas automáticas
    → Imágenes Gemini
    → Guiones automatizados
    → Videos compilados
    → Batch listo para TikTok

TÚ:
  Una vez/semana:
    → Revisar batch
    → Dar feedback (si cambios)
    → Upload a TikTok
```

---

## Detalles de Cada Bloque

### 1️⃣ BLOQUE SCRAPING

**Entrada:** Comando "scrapear"  
**Proceso:**
- Conectar a fuentes de noticias
- Extraer noticias últimos 7 días
- Filtrar por relevancia
- Guardar en DB

**Salida:** Lista de 5-10 noticias relevantes  
**Tiempo:** ~30-60 segundos

### 2️⃣ BLOQUE IDEAS

**Entrada:** Noticias scrapeadas  
**Proceso:**
- Para cada noticia
- Generar 2-3 conceptos de meme
- Usar preferencias aprendidas
- Mantener estilo "El Típico"

**Salida:** 10-15 ideas (2-3 por noticia)  
**Tiempo:** ~2-3 minutos

### 3️⃣ BLOQUE IMÁGENES

**Entrada:** Ideas aprobadas  
**Proceso:**
- Generar prompts optimizados
- Llamar Gemini Plus API
- Descargar imágenes
- Guardar en `/data/images`

**Salida:** 7 imágenes PNG  
**Tiempo:** ~2-3 minutos (Gemini es rápido)

### 4️⃣ BLOQUE GUIONES

**Entrada:** Imágenes + ideas  
**Proceso:**
- Para cada imagen
- Generar captions/texto
- Máx 280 caracteres
- Añadir hashtags trending

**Salida:** 7 guiones + hashtags  
**Tiempo:** ~1-2 minutos

### 5️⃣ BLOQUE VIDEOS

**Entrada:** Imágenes + guiones  
**Proceso:**
- Compilar con FFmpeg
- Resolución: 1080x1920
- Duración: 15-60 segundos
- Añadir efectos/transiciones
- Guardar en `/data/videos`
- Sync a Google Drive

**Salida:** 7 videos MP4  
**Tiempo:** ~5-10 minutos

### 6️⃣ BLOQUE FEEDBACK

**Entrada:** Videos compilados  
**Proceso:**
- Usuario ve videos
- Da feedback: ✅ / 🔶 / ❌
- Registra comentarios
- Sistema actualiza DB

**Salida:** Preferencias actualizadas  
**Tiempo:** ~5 minutos

---

## Système de Feedback

```
✅ BUENO
- Video excelente
- Usar este patrón próximas veces
- Incrementar relevancia

🔶 AJUSTAR
- Video OK pero mejorable
- Hacer cambios mínimos
- Feedback específico

❌ MALO
- Video no funciona
- No usar este patrón
- Evitar este tipo de contenido
```

---

## Base de Datos de Preferencias

Se actualiza automáticamente con cada feedback.

```json
{
  "temas_que_funcionan": [...],
  "estilos_efectivos": [...],
  "prompts_ganadores": [...],
  "metricas": {
    "tasa_exito": 0.75,
    "mejor_tema": "viento_canario",
    "peor_tema": "politics"
  }
}
```

Próximo batch usa estas preferencias para generar mejores videos.

---

## Checkpoints de Calidad

Cada bloque tiene un checkpoint de calidad:

1. **Scraping:** ¿Las noticias tienen sentido?
2. **Ideas:** ¿El concepto es humorístico?
3. **Imágenes:** ¿La imagen representa la idea?
4. **Guiones:** ¿El texto es máx 280 chars?
5. **Videos:** ¿Duración correcta y sin errores?

---

## Error Handling

Si algo falla:
- Registrar error en logs
- Mostrar al usuario
- Ofrecer alternativas
- Continuar con siguiente item

```
Error generando imagen 3 → Regenerar
Fallando Gemini API → Usar DALL-E fallback
Video dañado → Recompilar
```

---

## Performance Esperado

| Bloque | Duración | Items |
|--------|----------|-------|
| Scraping | 30-60s | 7 noticias |
| Ideas | 2-3m | 10-15 ideas |
| Imágenes | 2-3m | 7 imágenes |
| Guiones | 1-2m | 7 guiones |
| Videos | 5-10m | 7 videos |
| Feedback | 5m | 7 calificaciones |
| **TOTAL** | **~20-25m** | **7 videos completos** |

Puedes hacer 2-3 sesiones completas por hora si lo necesitas.
