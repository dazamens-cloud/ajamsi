# 📋 Especificación del Proyecto AjamSi

## Visión General

**AjamSi** es un sistema automático que convierte noticias de Canarias/Lanzarote en contenido humorístico para TikTok.

### Idea Core
- ✅ Scrapear noticias locales
- ✅ Generar ideas de memes automáticas
- ✅ Crear imágenes con IA (Gemini Plus)
- ✅ Generar guiones/captions
- ✅ Compilar videos automáticamente
- ✅ Aprender del feedback y mejorar

## Objetivo Comercial

| Métrica | Objetivo | Timeline |
|---------|----------|----------|
| Seguidores | 1K | 2-3 meses |
| Videos/semana | 5-7 | Mes 2 |
| Engagement rate | >5% | Mes 3 |
| Viabilidad monetaria | 100 USD/mes | Mes 4 |

## Isla Objetivo

**Lanzarote** - Tu isla

### Por qué Lanzarote
1. Contexto local único
2. Público objetivo específico
3. Noticias locales abundantes
4. Oportunidad de viralidad con contenido local

## Personaje Principal

**El Típico Canario**
- Vestuario tradicional
- Humor sardónico
- Referencia local constante
- Ilustración estilo folclórico

## Plataforma Principal

**TikTok** (@hummorkana)
- Algoritmo amigable para IA
- Monetización disponible (Creator Fund, patrocinios)
- Alcance global

### Posible Expansión
- Instagram Reels
- YouTube Shorts

## Monetización (Futuro)

### Fase 1 (0-1K seguidores)
- Acumular contenido
- Validar que funciona
- Sin monetización

### Fase 2 (1K-10K seguidores)
- TikTok Creator Fund (~$0.02-0.05 por 1K views)
- Patrocinios locales (restaurantes, hoteles)
- Merchandise básico

### Fase 3 (10K+ seguidores)
- Patrocinios de marcas
- Patreon/Ko-fi
- Promociones de servicios locales

## KPIs Principales

### Engagement
- Likes rate: >3%
- Share rate: >1%
- Comment rate: >0.5%
- Watch-through: >70%

### Crecimiento
- Followers/mes: +500 (objetivo)
- Videos/semana: 5-7
- Virales/mes: 1-2

### Calidad
- Videos completados exitosamente: >90%
- Feedback positivo: >70%
- Reutilización de patrones efectivos

## Restricciones & Consideraciones

### Legal
- ✅ Web scraping = Legal (Fair Use)
- ✅ Contenido original (no copiado)
- ✅ Declarar noticias de fuentes
- ✅ Cumplir términos de TikTok

### Técnicas
- No APIs pagas de Midjourney (solo Gemini Plus)
- FFmpeg local (sin límites)
- Google Drive para backup
- SQLite para persistencia

### Contenido
- ❌ Evitar política controversial
- ❌ Evitar contenido triste/negativo
- ❌ Evitar temas sensibles
- ✅ Humor local y accessible
- ✅ Referencia a noticias reales

## Fases del Proyecto

### FASE 0: Setup ✅ COMPLETADO
- Estructura del código
- Base de datos
- Configuración
- Git inicial

**Duración:** 1 sesión

### FASE 1: Implementación de Core 🔄 EN PROGRESO
- Web scraper funcional
- Generador de ideas
- Integración Gemini Plus
- Compilador de videos
- Sistema de feedback

**Duración estimada:** 2-3 semanas

**Deliverable:** 5-10 videos completos de prueba

### FASE 2: Validación 🔲 PENDIENTE
- Crear 15-20 videos completos
- Subirlos a TikTok
- Recolectar datos de engagement
- Validar que funciona
- Ajustar según resultados

**Duración estimada:** 4 semanas

**Criterio de éxito:**
- Si >500K views acumuladas = viable
- Si <100K views = pivotear

### FASE 3: Optimización 🔲 PENDIENTE
- Escalar a 5-7 videos/semana
- Automatización creciente
- Análisis de patrones
- Mejora continua

**Duración:** 6+ meses

## Riesgos & Mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|------------|--------|-----------|
| Algoritmo TikTok no viral | Media | Alto | Experimentar con múltiples formatos |
| Ban de scrapers | Baja | Alto | Respetar robots.txt, delays |
| Falta de noticias interesantes | Baja | Medio | Tener fuentes backup |
| Gemini Plus API limitaciones | Baja | Medio | Tener fallback a DALL-E |
| Pérdida de datos | Muy baja | Alto | Sync automático a Drive |

## Timeline General

```
Semana 1: FASE 0 ✅
Semanas 2-4: FASE 1 🔄
Semanas 5-8: FASE 2
Semana 9+: FASE 3 (si viable)
```

**Decisión de pivoteo:** Después de FASE 2, si viralidad <100K views, considerar:
- Cambio de tema
- Cambio de formato
- Cambio de plataforma
