# 📰 Fuentes de Noticias - Investigación Completa

> Investigación de todas las fuentes disponibles para scrapear

---

## 🔍 FUENTES ACTUALES (6)

### PRIORIDAD 1 - Lanzarote Específico (5 fuentes)

| Fuente | URL | Tipo | Estructura |
|--------|-----|------|-----------|
| **Lancelot Digital** | lancelotdigital.com/lanzarote | Portal de noticias | Artículos HTML estándar |
| **Crónicas de Lanzarote** | cronicasdelanzarote.es | Blog de crónicas | Artículos + comentarios |
| **Noticias de Lanzarote** | noticiasdelanzarote.com | Agregador local | Feed de noticias |
| **Diario de Lanzarote** | diariodelanzarote.com | Diario digital | Formato periódico |
| **El Periódico de Lanzarote** | elperiodicodelanzarote.com | Periódico digital | Artículos catalogados |

### PRIORIDAD 2 - Canarias General (1 fuente)

| Fuente | URL | Tipo | Estructura |
|--------|-----|------|-----------|
| **Canarias Ahora** | eldiario.es/canariasahora | Sección temática | Integrada en elDiario.es |

---

## 🔎 FUENTES POTENCIALES ADICIONALES

### Canarias Completo - Medios Tradicionales

| Fuente | URL | Audiencia | Notas |
|--------|-----|-----------|-------|
| **Canarias7** | canarias7.es | Periódico líder Canarias | Alto alcance, importante |
| **Diario de Avisos** | diariodeavisos.elespanol.com | Periódico español | Sección Canarias |
| **Diario de Canarias** | diariodecanarias.es | Periódico digital | Noticias generales Canarias |
| **ecanarias.net** | ecanarias.net | Portal de noticias | Histórico y confiable |
| **Canary Islands News** | canaryislandsnews.com | Noticias en inglés | Turismo y general |

### Redes Sociales & Plataformas Alternativas

#### ❌ Facebook
- **Problema:** Sin API pública para scraping desde 2018
- **Alternativa:** Búsqueda manual de grupos/páginas locales
- **Páginas importantes:**
  - "Lanzarote Noticias" (grupo privado/público)
  - "Información Lanzarote" (comunidad local)
  - Perfiles de periódicos locales
  
#### ❌ Twitter/X
- **Problema:** API pagada ($100/mes mínimo)
- **Alternativa:** Web scraping (pero frágil y cambiante)
- **Cuentas relevantes:**
  - @LancelotDigital
  - Periódicos locales
  - Medios canarios

#### ❓ Instagram
- **Problema:** Anti-scraping muy agresivo
- **Alternativa:** Ninguna viable
- **No recomendado:** Riesgo de ban

#### ✅ RSS Feeds (Si existen)
- **Ventaja:** Oficial y respeta Terms of Service
- **Problema:** Muchos sitios no publican feeds públicos
- **Alternativa:** Buscar feeds de cada periódico

---

## 📊 Análisis de Fuentes Potenciales

### Viabilidad de Scraping

```
FÁCIL ✅          INTERMEDIO 🟡         DIFÍCIL ❌
─────────────────────────────────────────────────
Sitios HTML       RSS Feeds              Facebook
estándar          (si existen)           Twitter/X (pago)
                                        Instagram
                  Bloggers              TikTok
                  (webs personales)
```

### Recomendación Actual

**Mantener las 6 actuales + Agregar 3 nuevas:**

1. ✅ **Canarias7** - Periódico más importante de Canarias
2. ✅ **ecanarias.net** - Más cobertura local
3. ✅ **Diario de Avisos** - Alcance español pero con Canarias

**Total: 9 fuentes (6 + 3)**

---

## 🚀 Sobre Facebook & Twitter

### Facebook Scraping - Análisis Detallado

**¿Por qué es difícil?**
- Facebook bloqueó API pública en 2018
- Anti-scraping muy agresivo
- Cambios constantes de estructura HTML
- Riesgo de ban de IP permanente

**Opciones teóricas:**
1. **Selenium + Firefox Headless** - Simula navegador real
   - Problema: Lento (5+ segundos por página)
   - Problema: Alto consumo de CPU/RAM
   - Riesgo: Facebook detecta bots

2. **API de Facebook con credenciales**
   - Costo: Requiere aprobación + dinero
   - Complejidad: Setup complicado
   - Viabilidad: Baja para proyecto personal

3. **Búsqueda manual de grupos/páginas**
   - Más viable: Identificar grupos locales
   - Problema: No automatizable

**Mi recomendación:** ❌ No vale la pena ahora
- Mejor usar las 9 fuentes web que son confiables
- Si hay mucho volumen después, reconsiderar

---

## 🐦 Twitter/X Scraping - Análisis

**¿Por qué es difícil?**
- Twitter obligó a API pagada ($100/mes mínimo)
- Web scraping es frágil (cambios frecuentes)
- Riesgo de ban de cuenta

**Opciones:**
1. **API de Twitter** ($100/mes)
   - Costo: No es viable para hobby
   - Beneficio: Confiable y rápido

2. **Web scraping (nitter.net)**
   - Nitter: Espejo de Twitter sin JS
   - Problema: Pueden bloquearlo
   - Riesgo: Medio-alto

3. **Hashtags de Canarias**
   - #Lanzarote #CanariasNews #Canarias
   - Problema: Ruido y bots

**Mi recomendación:** ⚠️ No prioritario
- Complejidad > Beneficio
- Las 9 webs dan suficiente volumen

---

## ✅ Plan Mejorado - 9 Fuentes

### Implementación en Orden:

#### FASE 1A - Actuales (ya configuradas)
1. ✅ Lancelot Digital
2. Crónicas de Lanzarote
3. Noticias de Lanzarote
4. Diario de Lanzarote
5. El Periódico de Lanzarote
6. Canarias Ahora

#### FASE 1B - Nuevas Agregadas (después de las 6)
7. 🆕 Canarias7
8. 🆕 ecanarias.net
9. 🆕 Diario de Avisos

### Volumen Esperado:

| Escenario | Noticias/semana | Suficiente para |
|-----------|-----------------|-----------------|
| 6 fuentes | 30-50 | 5-7 videos |
| 9 fuentes | 50-80 | 7-10 videos |

---

## 🎯 Solución Híbrida (Mi Propuesta)

**Por ahora (FASE 1):**
- Mantener 6 fuentes configuradas ✅
- Agregar 3 nuevas (Canarias7, ecanarias, Diario de Avisos)
- **Total: 9 fuentes web confiables**

**Futuro (FASE 3+):**
- Si necesitamos más volumen, considerar:
  - Búsqueda manual en grupos Facebook
  - Monitoreo de hashtags en Twitter (sin scraping)
  - Feeds RSS de otros periódicos

**No prioritario (nunca):**
- ❌ Facebook scraping automático
- ❌ Instagram scraping
- ❌ Twitter API pagada

---

## 📋 Alternativas Creativas

### 1. **Colaboradores Manuales**
Si Facebook es importante:
- Tener 2-3 personas que reporten noticias desde FB
- Añadirlas a un Telegram/Discord
- Tú lo copias manualmente al sistema

### 2. **Monitoreo de Hashtags**
```
#Lanzarote
#NoticiasLanzarote
#LanzaroteCultura
#LanzaroteDeporte
```
Búsqueda manual 1-2 veces/semana en redes

### 3. **Google Alerts**
```
Google Alerts para:
- "Lanzarote noticias"
- "Lanzarote evento"
- "Lanzarote turismo"
```
Te envía emails → Converts a noticias

### 4. **RSS Feeds Agregados**
```
Feedly o Inoreader:
- Agregar todos los feeds disponibles
- Exportar OPML
- Crear scraper de feeds RSS
```

---

## 🔧 Decisión: ¿Qué Hacemos?

### Opción A (RECOMENDADO): 9 Fuentes Web
- ✅ Fácil de implementar
- ✅ Confiable y legal
- ✅ Suficiente volumen
- ✅ Sin riesgos técnicos

### Opción B (ARRIESGADO): Agregar Facebook
- ❌ Riesgo de ban
- ❌ Lento y complejo
- ❌ Frágil (cambios constantes)
- ⚠️ No recomendado

### Opción C (HIBRIDA): 9 Webs + Manual desde FB
- ✅ Mejor de ambos mundos
- ✅ Sin automatización en FB
- ⚠️ Requiere trabajo manual

---

## ✅ DECISIÓN FINAL

**Opción elegida: A - 9 Fuentes Web**

**Estado:**
- ✅ 6 fuentes originales configuradas
- ✅ 3 nuevas fuentes agregadas y ACTIVADAS
- ❌ Facebook - DESCARTADO (riesgo alto, baja viabilidad)
- ❌ Twitter/X - DESCARTADO (API pagada, riesgo de ban)

**Total: 9 fuentes web confiables y legales**

---

### 📋 Fuentes Activas Finales

#### PRIORIDAD 1 - Lanzarote Específico (6 fuentes)
1. Lancelot Digital
2. Crónicas de Lanzarote
3. Noticias de Lanzarote
4. Diario de Lanzarote
5. El Periódico de Lanzarote
6. Canarias7 ⭐ NUEVA

#### PRIORIDAD 2 - Canarias General (3 fuentes)
7. Canarias Ahora
8. ecanarias.net ⭐ NUEVA
9. Diario de Avisos ⭐ NUEVA

**Volumen esperado:** 50-80 noticias/semana (suficiente para 7-10 videos)
