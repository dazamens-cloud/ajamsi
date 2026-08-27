# 📦 DEPENDENCIAS DE AJAMSI

**Fecha de revisión:** 2026-08-27  
**Versión:** 1.0

---

## ✅ CHECKLIST DE DEPENDENCIAS

### 🔴 CRÍTICAS (Requeridas)

- [ ] **Python 3.8+**
- [ ] **pip** (gestor de paquetes)
- [ ] **git** (opcional pero recomendado)

### 🟡 IMPORTANTES (Para scraping)

- [ ] **requests** (HTTP library)
- [ ] **beautifulsoup4** (HTML parsing)
- [ ] **lxml** (XML parsing, dependencia de beautifulsoup4)

### 🟡 IMPORTANTES (Para IA)

- [ ] **anthropic** (Claude API)

### 🟡 IMPORTANTES (Para videos)

- [ ] **FFmpeg** (video compilation)
- [ ] **ffmpeg-python** (Python wrapper)

### 🟠 OPCIONALES (Para Google Drive)

- [ ] **google-auth-oauthlib** (OAuth2)
- [ ] **google-auth-httplib2** (HTTP authentication)
- [ ] **google-api-python-client** (Google Drive API)

### 🟢 UTILIDADES

- [ ] **python-dotenv** (variables de entorno)

---

## 🖥️ PASO 1: Instalar Python

### Windows

#### Opción A: Instalador oficial (RECOMENDADO)
1. Ir a https://www.python.org/downloads/
2. Descargar Python 3.11 (última versión estable)
3. Ejecutar instalador
4. **✅ IMPORTANTE:** Marcar "Add Python to PATH"
5. Click "Install Now"

#### Opción B: Microsoft Store
1. Abre Microsoft Store
2. Busca "Python"
3. Click en la versión oficial
4. Click "Get"

#### Opción C: Chocolatey (si tienes)
```bash
choco install python
```

### Verificar instalación
```bash
python --version
pip --version
```

**Debe mostrar:**
```
Python 3.8.0 o superior
pip X.X.X
```

---

## 📦 PASO 2: Instalar Dependencias Python

### Opción A: Archivo requirements.txt (RECOMENDADO)

```bash
cd "D:\proyectos godot\tik tok\ajamsi"
pip install -r requirements.txt
```

### Opción B: Manual (si requirements.txt no funciona)

```bash
# Dependencias críticas
pip install requests
pip install beautifulsoup4
pip install lxml

# Claude API
pip install anthropic

# FFmpeg wrapper
pip install ffmpeg-python

# Google Drive (opcional)
pip install google-auth-oauthlib
pip install google-auth-httplib2
pip install google-api-python-client

# Utilidades
pip install python-dotenv
```

### Verificar instalación
```bash
python -c "import requests; import bs4; import anthropic; print('✓ Todas las librerías importan correctamente')"
```

---

## 🎬 PASO 3: Instalar FFmpeg

### Windows

#### Opción A: Installer (RECOMENDADO)
1. Ir a https://ffmpeg.org/download.html
2. Descargar versión Windows
3. Extraer a `C:\ffmpeg\`
4. Agregar `C:\ffmpeg\bin` al PATH

#### Opción B: Chocolatey
```bash
choco install ffmpeg
```

#### Opción C: Winget
```bash
winget install FFmpeg
```

#### Opción D: Manual (sin instalar)
1. Descargar build desde https://ffmpeg.org/download.html
2. Extraer a carpeta del proyecto
3. Actualizar main.py para usar ruta local

### Verificar instalación
```bash
ffmpeg -version
ffprobe -version
```

**Debe mostrar versiones de ambos.**

---

## 🔐 PASO 4: Configurar Google Drive (Opcional)

### Solo si quieres sincronización automática

#### A. Crear proyecto en Google Cloud

1. Ir a https://console.cloud.google.com/
2. Crear nuevo proyecto
3. Nombre: "AjamSi"
4. Click "Create"

#### B. Habilitar Google Drive API

1. En el proyecto, buscar "Google Drive API"
2. Click en el resultado
3. Click "Enable"

#### C. Crear Service Account

1. En Google Cloud Console, ir a "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Nombre: "ajamsi-service"
4. Crear
5. En la cuenta, ir a "Keys"
6. Click "Add Key" → "Create new key"
7. Tipo: JSON
8. Click "Create"
9. **Descargar archivo JSON**
10. Guardar como `credentials.json` en raíz del proyecto

#### D. Compartir carpeta con service account

1. Crear carpeta en Google Drive
2. Obtener email del service account (en credentials.json)
3. Compartir carpeta con ese email

### Verificar
```bash
python -c "
from google.oauth2.service_account import Credentials
creds = Credentials.from_service_account_file('credentials.json')
print('✓ Google Drive configurado')
"
```

---

## 🔑 PASO 5: Configurar Claude API Key

### Obtener API Key

1. Ir a https://console.anthropic.com/
2. Crear/loguear cuenta
3. Ir a "API Keys"
4. Click "Create Key"
5. Copiar la clave

### Guardar en .env

```bash
# Crear archivo .env en raíz del proyecto
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
```

### Verificar
```bash
python -c "
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
print('✓ Claude API configurado')
"
```

---

## 📋 CHECKLIST FINAL DE INSTALACIÓN

### Python & Pip
- [ ] `python --version` → 3.8+
- [ ] `pip --version` → pip X.X.X

### Dependencias Python
- [ ] `pip list` → contiene requests, beautifulsoup4, anthropic, ffmpeg-python

### FFmpeg
- [ ] `ffmpeg -version` → muestra versión
- [ ] `ffprobe -version` → muestra versión

### Google Drive (si aplica)
- [ ] `credentials.json` existe en raíz
- [ ] Service account tiene acceso a carpeta de Drive

### Claude API (si aplica)
- [ ] `.env` contiene ANTHROPIC_API_KEY
- [ ] API Key es válida

### Proyecto AjamSi
- [ ] `python -c "from src.pipeline import AjamSiPipeline; print('✓ Listo')"` funciona

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error: "ModuleNotFoundError: No module named 'requests'"

**Solución:**
```bash
pip install requests
```

### Error: "ffmpeg not found"

**Solución:**
1. Verificar FFmpeg instalado: `ffmpeg -version`
2. Si no existe, instalar según PASO 3
3. Asegurar que está en PATH

### Error: "No module named 'anthropic'"

**Solución:**
```bash
pip install anthropic
```

### Error: "Google Drive authentication failed"

**Solución:**
1. Verificar `credentials.json` existe
2. Verificar estructura del JSON
3. Verificar service account tiene permisos
4. Volver a descargar credentials.json si es necesario

### Error: "Python not found"

**Solución:**
1. Reinstalar Python con "Add to PATH" marcado
2. O agregar manualmente:
   - Buscar "Environment Variables" en Windows
   - Agregar ruta de Python al PATH
   - Ejemplo: `C:\Users\YourUser\AppData\Local\Programs\Python\Python311`

---

## ✅ VERIFICACIÓN COMPLETA

Ejecutar este script para verificar todo:

```bash
python -c "
print('=' * 60)
print('VERIFICACIÓN DE DEPENDENCIAS - AJAMSI v1.0')
print('=' * 60)
print()

# Python
import sys
print(f'✓ Python: {sys.version.split()[0]}')

# Librerías principales
try:
    import requests
    print('✓ requests')
except: print('✗ requests')

try:
    import bs4
    print('✓ beautifulsoup4')
except: print('✗ beautifulsoup4')

try:
    import anthropic
    print('✓ anthropic')
except: print('✗ anthropic')

try:
    import ffmpeg
    print('✓ ffmpeg-python')
except: print('✗ ffmpeg-python')

try:
    import google.oauth2
    print('✓ google-auth-oauthlib')
except: print('✗ google-auth-oauthlib (opcional)')

# FFmpeg ejecutable
import subprocess
try:
    subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
    print('✓ FFmpeg (ejecutable)')
except: print('✗ FFmpeg (ejecutable)')

# Google Drive credentials
import os
if os.path.exists('credentials.json'):
    print('✓ credentials.json')
else:
    print('⚠ credentials.json (opcional)')

print()
print('=' * 60)
print('VERIFICACIÓN COMPLETADA')
print('=' * 60)
"
```

---

## 📝 Resumen de Versiones Recomendadas

| Software | Versión Mínima | Versión Recomendada |
|----------|----------------|-------------------|
| Python | 3.8 | 3.11+ |
| pip | 20.0 | 23.0+ |
| FFmpeg | 4.0 | 6.0+ |
| requests | 2.25 | 2.31+ |
| beautifulsoup4 | 4.9 | 4.12+ |
| anthropic | 0.7 | 0.7+ |
| ffmpeg-python | 0.2 | 0.2+ |

---

## 🎯 Orden de Instalación Recomendado

1. **Python 3.11** (crítica)
2. **FFmpeg** (crítica para videos)
3. **pip install -r requirements.txt** (todas las librerías)
4. **credentials.json** (opcional, para Google Drive)
5. **.env** (opcional, para Claude API)

---

## ✨ Una vez instalado todo

```bash
# Verificar que todo funciona
cd "D:\proyectos godot\tik tok\ajamsi"

# Test rápido
python main.py

# O lanzar con script
lanzar.bat
```

**¡Listo para usar!** 🚀

---

## 📞 Soporte

Si algo no funciona:

1. Verificar error específico
2. Ver tabla "SOLUCIÓN DE PROBLEMAS"
3. Reinstalar software problemático
4. Verificar PATH de Windows
5. Contactar con documentación del software

**Todos los softwares son gratuitos y open-source.** ✅
