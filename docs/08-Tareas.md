# ✅ Tareas del Proyecto

## FASE 0: Setup Inicial ✅ COMPLETADO

- [x] Crear estructura de carpetas
- [x] Inicializar Git
- [x] Crear requirements.txt
- [x] Crear config.json
- [x] Crear DatabaseManager
- [x] Crear ConfigLoader
- [x] Script principal (main.py)
- [x] README.md
- [x] .gitignore y .env.example
- [x] Obsidian vault setup
- [x] Documentación en Obsidian

**Completado:** 2026-08-27  
**Duración:** 1 sesión

---

## FASE 1: Implementación de Core 🔄 EN PROGRESO

### Web Scraper Funcional (9 fuentes)
- [x] Crear módulo `base_scraper.py` (clase abstracta)
- [x] Crear módulo `scraper_manager.py` (orquestador)
- [x] Implementar scraping para Lancelot Digital ✅ COMPLETADO
- [ ] Implementar scraping para Crónicas de Lanzarote
- [ ] Implementar scraping para Noticias de Lanzarote
- [ ] Implementar scraping para Diario de Lanzarote
- [ ] Implementar scraping para El Periódico de Lanzarote
- [ ] Implementar scraping para Canarias7 (NEW)
- [ ] Implementar scraping para Canarias Ahora
- [ ] Implementar scraping para ecanarias.net (NEW)
- [ ] Implementar scraping para Diario de Avisos (NEW)
- [ ] Test de scraper con URLs reales
- [ ] Integración con DatabaseManager para guardar en DB

**Completado:** 11% (1 de 9 fuentes)  
**Estimado:** 3-4 días más (para las 8 fuentes restantes)  
**Prioridad:** 🔴 ALTA

**Estado Facebook/Twitter:** ❌ DESCARTADOS (visto riesgo/complejidad)

### Generador de Ideas
- [ ] Crear módulo `generators/idea_generator.py`
- [ ] Integrar Claude API
- [ ] Crear prompt optimizado para "El Típico"
- [ ] Sistema de contexto local (Lanzarote)
- [ ] Usar preferencias aprendidas
- [ ] Generar 2-3 conceptos por noticia
- [ ] Test con noticias de ejemplo

**Estimado:** 2-3 días  
**Prioridad:** 🔴 ALTA

### Integración Gemini Plus
- [ ] Crear módulo `generators/image_generator.py`
- [ ] Setup Gemini API credentials
- [ ] Prompt engineering para Gemini
- [ ] Descarga de imágenes
- [ ] Validación de imágenes (no corrupted)
- [ ] Fallback a DALL-E si Gemini falla
- [ ] Test de generación

**Estimado:** 2 días  
**Prioridad:** 🔴 ALTA

### Generador de Guiones
- [ ] Crear módulo `processors/caption_generator.py`
- [ ] Generar captions max 280 caracteres
- [ ] Búsqueda de hashtags trending
- [ ] Optimización para algoritmo TikTok
- [ ] Test con imágenes reales

**Estimado:** 1-2 días  
**Prioridad:** 🟡 MEDIA

### Compilador de Videos
- [ ] Crear módulo `processors/video_compiler.py`
- [ ] Integración FFmpeg
- [ ] Compilar imagen + audio + texto
- [ ] Efectos y transiciones
- [ ] Validación de duración (15-60s)
- [ ] Encoding MP4 para TikTok
- [ ] Test de compilación

**Estimado:** 2-3 días  
**Prioridad:** 🔴 ALTA

### Sistema de Feedback
- [ ] Crear módulo `utils/feedback_handler.py`
- [ ] Registrar feedback en DB
- [ ] Actualizar preferences.json
- [ ] Análisis de patrones ganadores
- [ ] Test del sistema

**Estimado:** 1-2 días  
**Prioridad:** 🟡 MEDIA

### Google Drive Sync
- [ ] Crear módulo `utils/drive_sync.py`
- [ ] Setup Google Drive API credentials
- [ ] Sync automático de imágenes
- [ ] Sync automático de videos
- [ ] Sync automático de bases de datos
- [ ] Test de sync

**Estimado:** 2 días  
**Prioridad:** 🟡 MEDIA

### Testing & QA
- [ ] Test unitarios para cada módulo
- [ ] Test de integración
- [ ] Test end-to-end
- [ ] Debugging y fixes

**Estimado:** 2-3 días  
**Prioridad:** 🟡 MEDIA

**Total Fase 1:** ~2-3 semanas  
**Deliverable:** 5-10 videos completos de prueba

---

## FASE 2: Validación 🔲 PENDIENTE

### Creación de Contenido
- [ ] Generar 5 videos (batch 1)
- [ ] Generar 5 videos (batch 2)
- [ ] Generar 5 videos (batch 3)
- [ ] Generar 5 videos (batch 4)
- [ ] Revisar todos (20 videos totales)

**Duración:** 4 semanas

### Publicación en TikTok
- [ ] Subir 20 videos a @hummorkana
- [ ] Spacing: 1-2 videos/día
- [ ] Monitoreo de views, likes, comments
- [ ] Recolectar métricas

**Duración:** 2-3 semanas (mientras subes en paralelo)

### Análisis de Resultados
- [ ] Calcular engagement rate
- [ ] Identificar videos que funcionan
- [ ] Identificar patrones fallidos
- [ ] Actualizar base de preferencias
- [ ] Generar report de viabilidad

**Duración:** 1 semana

### Criterio de Viabilidad
- ✅ Si >500K views acumuladas = VIABLE
- ❌ Si <100K views = PIVOTEAR

---

## FASE 3: Optimización 🔲 PENDIENTE

### Si VIABLE (>500K views)
- [ ] Escalar a 5-7 videos/semana
- [ ] Automatizar generación de ideas
- [ ] Mejorar compilación de videos
- [ ] Expandir a Instagram Reels
- [ ] Considerar monetización

**Duración:** 6+ meses

### Si NO VIABLE (<100K views)
- [ ] Pivotear tema (humor → educativo, etc.)
- [ ] Cambiar formato de videos
- [ ] Cambiar plataforma
- [ ] O dar por terminado proyecto

---

## Tareas Recurrentes

### Semanal
- [ ] Actualizar log de desarrollo
- [ ] Review de métricas
- [ ] Sesión de generación (5-7 videos)
- [ ] Análisis de feedback

### Diario (durante desarrollo)
- [ ] Revisar logs de errores
- [ ] Testing de cambios
- [ ] Documentar hallazgos

---

## Bloqueadores Actuales

| Bloqueador | Impacto | Solución |
|-----------|---------|----------|
| Ninguno | - | ✅ Todo setup |

---

## Próximas 48 Horas

1. [ ] Implementar web scraper básico
2. [ ] Test con URLs reales
3. [ ] Documentar learnings
4. [ ] Next: Generador de ideas
