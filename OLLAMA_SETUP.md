# 🎯 CONFIGURACIÓN DE OLLAMA - FASE 1

## ¿Qué es Ollama?

Ollama es un framework para ejecutar modelos de lenguaje localmente, sin necesidad de API keys ni conexión a servidores externos.

**Ventajas:**
- ✅ GRATIS (sin costo)
- ✅ 100% LOCAL (privacidad total)
- ✅ Sin límites de uso
- ✅ Sin latencia de red
- ✅ Funciona offline

## Instalación (Paso a Paso)

### 1. Descargar Ollama

Dirígete a: **https://ollama.ai** o **https://ollama.com**

Descarga el instalador para tu sistema operativo:
- **Windows**: ollama-windows-latest.exe
- **Mac**: ollama-macos-latest.zip
- **Linux**: Instrucciones en la web

### 2. Instalar Ollama

**Windows:**
```powershell
# Ejecuta el archivo .exe descargado
# Sigue el asistente de instalación
# Ollama se instalará en Program Files
```

**Mac:**
```bash
# Descomprime y copia a Applications
# O instala con Homebrew:
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Verificar Instalación

Abre terminal/PowerShell y ejecuta:

```bash
ollama --version
```

Deberías ver algo como: `ollama version 0.1.34`

## Descargar Modelos

Ollama necesita que descarges los modelos que quieras usar.

### Modelos Recomendados (por velocidad/calidad):

**Para prompts creativos (RECOMENDADO):**
```bash
ollama pull mistral
# o
ollama pull neural-chat
```

**Alternativas:**
```bash
ollama pull llama2        # Más completo, más lento
ollama pull qwen:latest   # Muy bueno en creatividad
ollama pull dolphin-mixtral  # Rápido y preciso
```

### Descargar modelo:

```bash
ollama pull mistral
```

Esto descargará ~4-5GB (depende del modelo). La primera vez tarda más.

## Ejecutar Ollama

### Opción A: Iniciar el servidor (RECOMENDADO)

Abre PowerShell y ejecuta:

```powershell
ollama serve
```

O si instalaste con script:
```bash
ollama serve
```

Deberías ver:
```
listening on 127.0.0.1:11434
```

**⚠️ Importante:** Deja esta ventana abierta. Ollama escucha en http://localhost:11434

### Opción B: Ejecutar en background (Windows)

Si quieres que Ollama se ejecute siempre en background:

```powershell
# Crear tarea programada en Windows
schtasks /create /tn "OllamaServer" /tr "ollama serve" /sc onlogon /rl highest
```

## Verificar Conexión

### Desde PowerShell:

```powershell
# Verificar que Ollama responde
Invoke-WebRequest -Uri "http://localhost:11434/api/tags"
```

Deberías recibir JSON con los modelos descargados.

### Desde Python:

```python
import requests

response = requests.get("http://localhost:11434/api/tags", timeout=2)
if response.status_code == 200:
    print("✅ Ollama está disponible")
    print(response.json())
else:
    print("❌ Error conectando a Ollama")
```

## Usar en AJAMSI

Una vez que Ollama está corriendo, el sistema automáticamente:

1. **Detecta** si Ollama está disponible
2. **Genera prompts creativos** usando el modelo local
3. **Fallback automático** a templates si Ollama no responde

### Configuración en config.json:

```json
"prompt_engineer": {
  "proveedor": "ollama",
  "modelo": "mistral:latest",
  "temperatura": 0.7,
  "ollama_url": "http://localhost:11434"
}
```

## Resolver Problemas

### "Connection refused" o "404"

**Solución:**
1. Verifica que Ollama está corriendo (`ollama serve`)
2. Verifica puerto: `netstat -tuln | grep 11434` (Linux) o `netstat -ano | find "11434"` (Windows PowerShell)
3. Intenta manualmente: `Invoke-WebRequest -Uri "http://localhost:11434/api/tags"`

### "Model not found"

**Solución:**
1. Lista modelos descargados: `ollama list`
2. Descarga modelo: `ollama pull mistral`
3. Verifica config.json tenga nombre correcto

### Lentitud

**Solución:**
1. Asigna más RAM a Ollama (Windows: Properties → Advanced)
2. Usa modelo más pequeño: `neural-chat` < `mistral` < `llama2`
3. GPU: Si tienes NVIDIA, Ollama puede usar CUDA para acelerar

## Comandos Útiles

```bash
# Ver modelos descargados
ollama list

# Descargar modelo
ollama pull [nombre]

# Ejecutar interactivo
ollama run mistral

# Ver información del sistema
ollama info

# Eliminar modelo
ollama rm mistral

# Ver logs
ollama logs
```

## Modelos por Caso de Uso

| Modelo | Velocidad | Creatividad | RAM | Mejor Para |
|--------|-----------|-----------|-----|-----------|
| neural-chat | ⚡⚡⚡ | ⭐⭐ | 4GB | Chat rápido |
| mistral | ⚡⚡ | ⭐⭐⭐ | 7GB | **Prompts (RECOMENDADO)** |
| qwen:latest | ⚡ | ⭐⭐⭐⭐ | 6GB | Creatividad máxima |
| llama2 | ⚡ | ⭐⭐⭐ | 7GB | Versatilidad |
| dolphin-mixtral | ⚡⚡ | ⭐⭐⭐ | 8GB | Instructivo |

## Próximos Pasos

✅ Instala Ollama
✅ Descarga `mistral`
✅ Ejecuta `ollama serve`
✅ El orquestador AJAMSI detectará automáticamente Ollama
✅ ¡Genera prompts sin costo!

## Soporte

Si encuentras problemas:
1. Verifica: https://ollama.ai/troubleshooting
2. Logs de Ollama: `ollama logs`
3. GitHub Issues: https://github.com/ollama/ollama/issues

---

**Estado Actual AJAMSI:**
- Prompt Engineer: ✅ USA OLLAMA (FASE 1 completado)
- Scraper: ⏳ Próximo (FASE 2)
- Video Creator: ⏳ Próximo (FASE 3)
