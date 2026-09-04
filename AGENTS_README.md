# 🤖 AJAMSI Agents - Sistema de 10 Agentes Especializados

> **Estado:** ✅ Implementado y listo para usar  
> **Fecha:** 2026-08-30  
> **Versión:** 1.0.0

---

## 📋 Índice

1. [Visión General](#visión-general)
2. [Los 10 Agentes](#los-10-agentes)
3. [Guía de Uso](#guía-de-uso)
4. [Ejemplos Prácticos](#ejemplos-prácticos)
5. [Flujo de Trabajo](#flujo-de-trabajo)

---

## 🎯 Visión General

El sistema de agentes de AjamSi divide el pipeline de generación de contenido en **10 agentes especializados** que trabajan coordinadamente para convertir noticias en videos de TikTok.

### Estructura de Carpetas

```
ajamsi/
├── src/agents/                          ← 10 AGENTES AQUÍ
│   ├── scraper_agent.py                 (1️⃣)
│   ├── idea_generator_agent.py           (2️⃣)
│   ├── prompt_engineer_agent.py          (3️⃣)
│   ├── video_compiler_agent.py           (4️⃣)
│   ├── caption_writer_agent.py           (5️⃣)
│   ├── batch_processor_agent.py          (6️⃣)
│   ├── feedback_analyzer_agent.py        (7️⃣)
│   ├── content_validator_agent.py        (8️⃣)
│   ├── analytics_agent.py                (9️⃣)
│   └── drive_sync_agent.py               (🔟)
│
├── agent_orchestrator.py                 ← ORQUESTADOR CENTRAL
└── test_orchestrator.py                  ← ARCHIVO DE PRUEBA
```

---

## 🤖 Los 10 Agentes

### 1️⃣ **SCRAPER AGENT** 🕷️
**Archivo:** `src/agents/scraper_agent.py`

**Responsabilidad:** Web scraping de noticias de Lanzarote

**Métodos principales:**
```python
scraper = ScraperAgent(config)
resultado = scraper.ejecutar(dias_atras=7, limite_noticias=20)
```

**Output:**
```python
{
    'status': 'success',
    'noticias_encontradas': 15,
    'noticias': [
        {
            'id': '...',
            'titulo': 'Noticia de Lanzarote',
            'url': '...',
            'contenido': '...',
            'fecha_publicacion': '...',
            'relevancia_score': 85.5
        },
        ...
    ]
}
```

---

### 2️⃣ **IDEA GENERATOR AGENT** 💡
**Archivo:** `src/agents/idea_generator_agent.py`

**Responsabilidad:** Generar conceptos creativos y ángulos humorísticos

**Métodos principales:**
```python
idea_gen = IdeaGeneratorAgent(config)
resultado = idea_gen.ejecutar(noticia, num_ideas=3)
```

**Output:**
```python
{
    'status': 'success',
    'ideas_generadas': 3,
    'ideas': [
        {
            'id': '...',
            'noticia_id': '...',
            'concepto': 'El Típico reaccionando a...',
            'angulo_humor': 'sardónico',
            'palabras_clave': ['lanzarote', 'viento'],
            'relevancia': 0.80
        },
        ...
    ]
}
```

---

### 3️⃣ **PROMPT ENGINEER AGENT** 🎨
**Archivo:** `src/agents/prompt_engineer_agent.py`

**Responsabilidad:** Optimizar prompts para Gemini Plus

**Métodos principales:**
```python
prompt_eng = PromptEngineerAgent(config)
resultado = prompt_eng.ejecutar(idea, num_prompts=3)
```

**Output:**
```python
{
    'status': 'success',
    'prompts_generados': 3,
    'prompts': [
        {
            'numero': 1,
            'estilo': 'folclórico',
            'prompt_text': 'El Típico Canario...',
            'para_copiar': '...'  # Listo para copiar-pegar en Gemini
        },
        ...
    ]
}
```

---

### 4️⃣ **VIDEO COMPILER AGENT** 🎬
**Archivo:** `src/agents/video_compiler_agent.py`

**Responsabilidad:** Compilación de videos con FFmpeg

**Métodos principales:**
```python
video_comp = VideoCompilerAgent(config)
resultado = video_comp.ejecutar(
    imagen_path='path/to/image.png',
    guion='Texto del video',
    audio_path='path/to/audio.mp3',
    duracion=30,
    formato='tiktok'
)
```

**Formatos soportados:**
- `tiktok` - 1080x1920, 30 fps
- `instagram` - 1080x1080, 30 fps
- `youtube` - 1920x1080, 60 fps

---

### 5️⃣ **CAPTION WRITER AGENT** ✍️
**Archivo:** `src/agents/caption_writer_agent.py`

**Responsabilidad:** Generar captions y hashtags optimizados

**Métodos principales:**
```python
caption_w = CaptionWriterAgent(config)
resultado = caption_w.ejecutar(idea, num_captions=3)
```

**Output:**
```python
{
    'status': 'success',
    'captions_generados': 3,
    'captions': [
        {
            'tipo': 'hook',
            'caption': 'Espera el final 👀 ...',
            'hashtags': '#Lanzarote #Canarias #Humor',
            'caracteres': 145,
            'dentro_limite': True
        },
        ...
    ]
}
```

---

### 6️⃣ **BATCH PROCESSOR AGENT** ⚙️
**Archivo:** `src/agents/batch_processor_agent.py`

**Responsabilidad:** Orquestar todos los agentes en bloques completos

**Métodos principales:**
```python
batch_proc = BatchProcessorAgent(config, agentes)
resultado = batch_proc.ejecutar_batch_completo('nombre_batch')
```

**Fases del batch:**
1. Scraping → 2. Ideas → 3. Prompts → 4. Captions → 5. Videos → 6. Validación → 7. Sync

---

### 7️⃣ **FEEDBACK ANALYZER AGENT** 📊
**Archivo:** `src/agents/feedback_analyzer_agent.py`

**Responsabilidad:** Analizar feedback y actualizar preferencias

**Métodos principales:**
```python
feedback_a = FeedbackAnalyzerAgent(config)
resultado = feedback_a.ejecutar({
    1: '✅',  # Video 1 positivo
    2: '❌',  # Video 2 negativo
    3: '🔶'   # Video 3 neutral
})
```

**Output:**
```python
{
    'status': 'success',
    'videos_positivos': 5,
    'videos_negativos': 2,
    'tasa_exito': 71.4,
    'patrones_identificados': ['Alta tasa de éxito', ...],
    'recomendaciones': ['Continuar con estilo actual', ...]
}
```

---

### 8️⃣ **CONTENT VALIDATOR AGENT** ✔️
**Archivo:** `src/agents/content_validator_agent.py`

**Responsabilidad:** Validar contenido antes de publicar

**Métodos principales:**
```python
validator = ContentValidatorAgent(config)
resultado = validator.ejecutar({
    'caption': 'Tu caption aquí',
    'duracion_segundos': 30,
    'concepto': 'Idea del video'
})
```

**Output:**
```python
{
    'status': 'success',
    'todo_ok': True,
    'puntuacion_calidad': 95,
    'recomendacion': 'LISTO PARA PUBLICAR',
    'alertas': []
}
```

---

### 9️⃣ **ANALYTICS AGENT** 📈
**Archivo:** `src/agents/analytics_agent.py`

**Responsabilidad:** Analizar métricas y rendimiento

**Métodos principales:**
```python
analytics = AnalyticsAgent(config)
resultado = analytics.ejecutar(periodo='semanal')
```

**Output:**
```python
{
    'status': 'success',
    'periodo': 'semanal',
    'resumen': {
        'total_videos': 24,
        'total_views': 15240,
        'engagement_rate': 5.6
    },
    'tendencias': ['📈 Aumento 23%', ...],
    'predicciones': {...}
}
```

---

### 🔟 **DRIVE SYNC AGENT** ☁️
**Archivo:** `src/agents/drive_sync_agent.py`

**Responsabilidad:** Sincronización automática con Google Drive

**Métodos principales:**
```python
drive_sync = DriveSyncAgent(config)
resultado = drive_sync.ejecutar({'archivos': 15})
```

**Output:**
```python
{
    'status': 'success',
    'archivos_sincronizados': 15,
    'tamaño_mb': 37.5,
    'estado': 'sincronizado',
    'proxima_sync': '...'
}
```

---

## 📖 Guía de Uso

### Instalación

```bash
cd D:\proyectos godot\tik tok\ajamsi

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Uso Básico - Desde la Terminal

#### 1️⃣ Inicializar el Orquestador

```python
from agent_orchestrator import AgentOrchestrator

# Inicializar con todos los 10 agentes
orquestador = AgentOrchestrator()
```

#### 2️⃣ Ejecutar Batch Completo (RECOMENDADO)

```python
# Ejecutar todo de una vez
resultado = orquestador.ejecutar_batch_completo("mi_batch")
```

#### 3️⃣ Usar Agentes Individuales

```python
# Scrappear noticias
noticias = orquestador.scrappear_noticias(dias_atras=7)

# Generar ideas
ideas = orquestador.generar_ideas(noticias[0], num_ideas=3)

# Optimizar prompts
prompts = orquestador.optimizar_prompts(ideas[0], num_prompts=3)

# Generar captions
captions = orquestador.generar_captions(ideas[0], num_captions=3)

# Validar contenido
validacion = orquestador.validar_contenido(content_dict)

# Analizar feedback
feedback = orquestador.analizar_feedback({1: '✅', 2: '❌'})

# Generar analytics
reportes = orquestador.generar_analytics(periodo='semanal')

# Sincronizar con Drive
sync = orquestador.sincronizar_drive({'archivos': 15})
```

---

## 💻 Ejemplos Prácticos

### Ejemplo 1: Ejecutar Batch Completo

```python
from agent_orchestrator import AgentOrchestrator

orquestador = AgentOrchestrator()

# Ejecutar batch
resultado = orquestador.ejecutar_batch_completo("batch_29_agosto")

print(f"Noticias: {resultado['estadisticas']['noticias_procesadas']}")
print(f"Ideas: {resultado['estadisticas']['ideas_generadas']}")
print(f"Videos prontos: {resultado['estadisticas']['videos_prontos']}")
```

### Ejemplo 2: Workflow Manual

```python
# Paso 1: Scrappear
noticias = orquestador.scrappear_noticias()['noticias']

# Paso 2: Para cada noticia, generar ideas
for noticia in noticias[:5]:
    ideas = orquestador.generar_ideas(noticia, num_ideas=3)['ideas']
    
    # Paso 3: Para cada idea, generar prompts
    for idea in ideas:
        prompts = orquestador.optimizar_prompts(idea)['prompts']
        captions = orquestador.generar_captions(idea)['captions']
        
        print(f"Idea: {idea['concepto']}")
        print(f"  Prompts: {len(prompts)}")
        print(f"  Captions: {len(captions)}")
```

### Ejemplo 3: Análisis de Feedback

```python
# Después de publicar 7 videos
feedback = {
    1: '✅',  # Video 1 funcionó bien
    2: '✅',
    3: '❌',  # Video 3 no funcionó
    4: '✅',
    5: '🔶',  # Video 5 fue neutral
    6: '✅',
    7: '❌',
}

resultado = orquestador.analizar_feedback(feedback)
print(f"Tasa de éxito: {resultado['tasa_exito']:.1f}%")
print(f"Recomendaciones: {resultado['analisis']['recomendaciones']}")
```

---

## 🔄 Flujo de Trabajo Completo

```
SESIÓN TÍPICA:

Paso 1: Inicializar
├─ orquestador = AgentOrchestrator()

Paso 2: Ejecutar Batch Completo
├─ resultado = orquestador.ejecutar_batch_completo()
│
│  Internamente ejecuta:
│  ├─ 1️⃣ Scraper: Raspa 7 días de noticias → 12 noticias
│  ├─ 2️⃣ Idea Generator: Genera 3 ideas por noticia → 36 ideas
│  ├─ 3️⃣ Prompt Engineer: Genera 2 prompts por idea → 72 prompts
│  ├─ 4️⃣ Caption Writer: Genera 3 captions por idea → 108 captions
│  ├─ 5️⃣ Video Compiler: Espera imágenes de Gemini
│  ├─ 6️⃣ Content Validator: Valida todo
│  ├─ 7️⃣ Drive Sync: Sube a Google Drive
│  └─ Listo para publicar

Paso 3: Tú generas imágenes en Gemini (MANUAL)
├─ Copia los prompts → Gemini Plus
├─ Descarga imágenes PNG

Paso 4: Compilar videos (MANUAL O AUTOMÁTICO)
├─ orquestador.compilar_video(imagen, guion, formato='tiktok')

Paso 5: Dar feedback
├─ feedback = {1: '✅', 2: '❌', ...}
├─ orquestador.analizar_feedback(feedback)
├─ Sistema aprende y mejora

Paso 6: Subir a TikTok (MANUAL)
├─ Videos listos en Google Drive
├─ Sube a @hummorkana

Paso 7: Analytics
├─ orquestador.generar_analytics(periodo='semanal')
└─ Ver qué funcionó mejor
```

---

## 🚀 Próximas Integraciones

### Obligatorias
- [ ] Google Drive API (credenciales)
- [ ] Gemini Plus API (imagen)
- [ ] BeautifulSoup (web scraping real)
- [ ] SQLite (base de datos)

### Opcionales
- [ ] FFmpeg (compilación local)
- [ ] TikTok API (si disponible)
- [ ] Telegram Bot (notificaciones)
- [ ] Scheduler (batches automáticos)

---

## 📞 Contacto y Soporte

**Proyecto:** AjamSi  
**Isla:** Lanzarote, Canarias  
**Cuenta TikTok:** @hummorkana  
**Última actualización:** 2026-08-30

---

✨ **Sistema listo para ser usado. ¡A generar contenido! 🚀**
