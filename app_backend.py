"""
AJAMSI - Backend API Flask
API para ejecutar el pipeline de manera interactiva
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sys
import os
from pathlib import Path
import json
import threading
from datetime import datetime
import tempfile

# Windows: evitar crashes de cp1252 al imprimir emojis en consola
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent_orchestrator import AgentOrchestrator
from utils.config_loader import ConfigLoader
from agents.health_check_agent import HealthCheckAgent

app = Flask(__name__)
CORS(app)

# Estado global
state = {
    'status': 'idle',  # idle, loading, ready
    'current_phase': 0,  # 0: init, 1: scraping, 2: ideas, 3: captions, 4: video
    'noticias': [],
    'noticias_indices_seleccionadas': [],  # Índices de noticias seleccionadas
    'noticia_seleccionada': None,
    'ideas': [],
    'ideas_seleccionadas': [],  # Ideas seleccionadas/corregidas
    'prompts': [],
    'captions': [],
    'captions_seleccionados': [],  # Captions seleccionados/corregidos
    'video': None,
    'error': None,
    'timestamp': None,
    'progress': {
        'activo': False,
        'porcentaje': 0,
        'paso': '',
        'detalle': '',
        'logs': [],
    },
    'resultado_final': None,
}

orquestador = None
VIDEOS_DIR = Path(__file__).parent / "videos"

@app.route('/')
def index():
    """Sirve el dashboard principal"""
    try:
        html_path = Path(__file__).parent / 'app_dashboard.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        return f"<h1>Error cargando dashboard: {e}</h1>", 500

@app.route('/studio')
def studio():
    """Interfaz PWA original (editor de detalles)"""
    try:
        html_path = Path(__file__).parent / 'app_frontend.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        return f"<h1>Error cargando PWA: {e}</h1>", 500

@app.route('/api/init', methods=['GET'])
def init_system():
    """Inicializar el orquestador"""
    global orquestador
    try:
        state['status'] = 'loading'
        config_loader = ConfigLoader("config/config.json")
        config = config_loader.to_dict()
        orquestador = AgentOrchestrator()
        state['status'] = 'ready'
        state['current_phase'] = 1
        return jsonify({
            'status': 'success',
            'message': '10 agentes inicializados',
            'state': state
        })
    except Exception as e:
        state['status'] = 'error'
        state['error'] = str(e)
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/phase1', methods=['POST'])
def phase1_scraping():
    """FASE 1: Scraping de noticias"""
    if not orquestador:
        return jsonify({'status': 'error', 'error': 'Orquestador no inicializado'}), 400

    def run_scraping():
        try:
            state['status'] = 'loading'
            print("🕷️  Iniciando scraping...")
            resultado = orquestador.scrappear_noticias(dias_atras=7)
            noticias = resultado.get('noticias', [])
            state['noticias'] = noticias
            state['current_phase'] = 1
            state['status'] = 'ready'
            state['timestamp'] = datetime.now().isoformat()
            print(f"✅ {len(noticias)} noticias obtenidas")
        except Exception as e:
            state['error'] = str(e)
            state['status'] = 'error'
            print(f"❌ Error: {e}")

    thread = threading.Thread(target=run_scraping)
    thread.start()

    return jsonify({
        'status': 'loading',
        'message': 'Scraping iniciado...'
    })

@app.route('/api/phase2', methods=['POST'])
def phase2_ideas():
    """FASE 2: Generar ideas y prompts"""
    if not orquestador:
        return jsonify({'status': 'error', 'error': 'Orquestador no inicializado'}), 400

    data = request.json
    noticia_idx = data.get('noticia_idx', 0)

    if noticia_idx >= len(state['noticias']):
        return jsonify({'status': 'error', 'error': 'Noticia no válida'}), 400

    def run_phase2():
        try:
            state['status'] = 'loading'
            noticia = state['noticias'][noticia_idx]
            state['noticia_seleccionada'] = noticia

            print(f"💡 Generando ideas para: {noticia.get('titulo', '')[:50]}...")
            ideas_resultado = orquestador.generar_ideas(noticia, num_ideas=2)
            ideas = ideas_resultado.get('ideas', [])
            state['ideas'] = ideas if isinstance(ideas, list) else [ideas]

            print(f"🎨 Generando prompts con Ollama...")
            if state['ideas']:
                idea = state['ideas'][0]
                prompts_resultado = orquestador.optimizar_prompts(idea, num_prompts=2)
                prompts = prompts_resultado.get('prompts', [])
                state['prompts'] = prompts

            state['current_phase'] = 2
            state['status'] = 'ready'
            state['timestamp'] = datetime.now().isoformat()
            print(f"✅ FASE 2 completada")
        except Exception as e:
            state['error'] = str(e)
            state['status'] = 'error'
            print(f"❌ Error: {e}")

    thread = threading.Thread(target=run_phase2)
    thread.start()

    return jsonify({
        'status': 'loading',
        'message': 'Generando ideas y prompts...'
    })

@app.route('/api/phase3', methods=['POST'])
def phase3_captions():
    """FASE 3: Generar captions"""
    if not orquestador or not state['ideas']:
        return jsonify({'status': 'error', 'error': 'No hay ideas para procesar'}), 400

    def run_phase3():
        try:
            state['status'] = 'loading'
            idea = state['ideas'][0]

            print(f"✍️  Generando captions...")
            captions_resultado = orquestador.generar_captions(idea, num_captions=3)
            captions = captions_resultado.get('captions', [])
            state['captions'] = captions

            state['current_phase'] = 3
            state['status'] = 'ready'
            state['timestamp'] = datetime.now().isoformat()
            print(f"✅ FASE 3 completada")
        except Exception as e:
            state['error'] = str(e)
            state['status'] = 'error'
            print(f"❌ Error: {e}")

    thread = threading.Thread(target=run_phase3)
    thread.start()

    return jsonify({
        'status': 'loading',
        'message': 'Generando captions...'
    })

@app.route('/api/phase4', methods=['POST'])
def phase4_video():
    """FASE 4: Compilar video"""
    if not orquestador:
        return jsonify({'status': 'error', 'error': 'Orquestador no inicializado'}), 400

    def run_phase4():
        try:
            state['status'] = 'loading'
            imagen_path = str(Path(__file__).parent / "imagenes" / "el_tipico_canario.png")

            print(f"🎬 Compilando video...")
            video_resultado = orquestador.compilar_video(
                imagen_path=imagen_path,
                guion="El Típico reaccionando a noticias",
                audio_path=None,
                formato='tiktok'
            )

            state['video'] = video_resultado
            state['current_phase'] = 4
            state['status'] = 'ready'
            state['timestamp'] = datetime.now().isoformat()
            print(f"✅ FASE 4 completada")
        except Exception as e:
            state['error'] = str(e)
            state['status'] = 'error'
            print(f"❌ Error: {e}")

    thread = threading.Thread(target=run_phase4)
    thread.start()

    return jsonify({
        'status': 'loading',
        'message': 'Compilando video...'
    })

@app.route('/api/phase1-get-results', methods=['GET'])
def phase1_get_results():
    """Obtener noticias de Fase 1 para selección"""
    return jsonify({
        'noticias': state['noticias'],
        'seleccionadas': state['noticias_indices_seleccionadas'],
        'total': len(state['noticias'])
    })

@app.route('/api/phase1-select', methods=['POST'])
def phase1_select():
    """Guardar selección de noticias"""
    data = request.json
    indices = data.get('indices', [])

    # Validar indices
    if not all(isinstance(i, int) and 0 <= i < len(state['noticias']) for i in indices):
        return jsonify({'status': 'error', 'error': 'Índices inválidos'}), 400

    state['noticias_indices_seleccionadas'] = indices
    state['noticia_seleccionada'] = state['noticias'][indices[0]] if indices else None

    return jsonify({
        'status': 'success',
        'noticias_seleccionadas': len(indices),
        'mensaje': f'{len(indices)} noticias seleccionadas'
    })

@app.route('/api/phase2-get-results', methods=['GET'])
def phase2_get_results():
    """Obtener ideas de Fase 2 para revisión/corrección"""
    return jsonify({
        'ideas': state['ideas'],
        'prompts': state['prompts'],
        'corregidas': state['ideas_seleccionadas'],
        'total_ideas': len(state['ideas']),
        'total_prompts': len(state['prompts'])
    })

@app.route('/api/phase2-correct', methods=['POST'])
def phase2_correct():
    """Guardar ideas y prompts corregidos"""
    data = request.json
    ideas_corregidas = data.get('ideas', [])

    state['ideas_seleccionadas'] = ideas_corregidas

    return jsonify({
        'status': 'success',
        'ideas_guardadas': len(ideas_corregidas),
        'mensaje': f'{len(ideas_corregidas)} ideas guardadas'
    })

@app.route('/api/phase3-get-results', methods=['GET'])
def phase3_get_results():
    """Obtener captions de Fase 3 para revisión/corrección"""
    return jsonify({
        'captions': state['captions'],
        'corregidos': state['captions_seleccionados'],
        'total_captions': len(state['captions'])
    })

@app.route('/api/phase3-correct', methods=['POST'])
def phase3_correct():
    """Guardar captions corregidos"""
    data = request.json
    captions_corregidos = data.get('captions', [])

    state['captions_seleccionados'] = captions_corregidos

    return jsonify({
        'status': 'success',
        'captions_guardados': len(captions_corregidos),
        'mensaje': f'{len(captions_corregidos)} captions guardados'
    })

@app.route('/api/run-all', methods=['POST'])
def run_all():
    """PIPELINE: procesa todas las noticias seleccionadas

    Query params:
    - modo: 'imagen' (default) = solo imágenes
    - modo: 'video' = genera videos también
    """
    if not orquestador:
        return jsonify({'status': 'error', 'error': 'Orquestador no inicializado'}), 400

    indices = state['noticias_indices_seleccionadas']
    if not indices:
        return jsonify({'status': 'error', 'error': 'No hay noticias seleccionadas'}), 400
    if state['progress']['activo']:
        return jsonify({'status': 'error', 'error': 'Ya hay un pipeline en ejecución'}), 400

    modo = request.args.get('modo', 'imagen').lower()
    generar_video = modo == 'video'
    noticias = [state['noticias'][i] for i in indices]

    def progreso_cb(pct, paso, detalle):
        state['progress']['porcentaje'] = pct
        state['progress']['paso'] = paso
        state['progress']['detalle'] = detalle
        state['progress']['logs'].append({
            'hora': datetime.now().strftime('%H:%M:%S'),
            'pct': pct, 'paso': paso, 'detalle': detalle,
        })
        state['progress']['logs'] = state['progress']['logs'][-50:]

    def run_pipeline():
        try:
            state['status'] = 'loading'
            state['progress']['activo'] = True
            state['progress']['porcentaje'] = 0
            state['progress']['logs'] = []
            state['error'] = None
            state['resultado_final'] = None

            resultado = orquestador.ejecutar_pipeline_completo(noticias, progreso_cb, generar_video)

            # Serializar resultado (sin objetos no serializables)
            state['resultado_final'] = {
                'status': resultado['status'],
                'imagenes_generadas': resultado.get('imagenes_generadas', 0),
                'videos_generados': resultado.get('videos_generados', 0),
                'doc_path': resultado['doc_path'],
                'errores': resultado['errores'],
                'items': [
                    {
                        'titulo': r['noticia'].get('titulo', ''),
                        'video_filename': (r.get('video') or {}).get('video_filename'),
                        'video_path': (r.get('video') or {}).get('video_path'),
                        'tamaño_mb': (r.get('video') or {}).get('tamaño_mb'),
                        'duracion': (r.get('video') or {}).get('duracion_segundos'),
                        'imagen_filename': (r.get('imagen') or {}).get('imagen_filename'),
                        'imagen_path': (r.get('imagen') or {}).get('imagen_path'),
                        'caption_recomendado': max(
                            r.get('captions', []),
                            key=lambda c: c.get('engagement_score', 0)
                        ).get('caption_completo', '') if r.get('captions') else '',
                    }
                    for r in resultado['resultados']
                ],
            }
            state['current_phase'] = 4
            state['status'] = 'ready'
            state['timestamp'] = datetime.now().isoformat()

            # Abrir carpeta automáticamente (Windows)
            if resultado.get('imagenes_generadas', 0) > 0:
                try:
                    os.startfile(str(VIDEOS_DIR))
                except Exception as e:
                    print(f"No se pudo abrir la carpeta: {e}")

        except Exception as e:
            state['error'] = str(e)
            state['status'] = 'error'
            print(f"❌ Error en pipeline: {e}")
        finally:
            state['progress']['activo'] = False

    thread = threading.Thread(target=run_pipeline)
    thread.start()

    msg_modo = "solo imágenes" if not generar_video else "imágenes + videos"
    return jsonify({
        'status': 'loading',
        'message': f'Pipeline iniciado ({msg_modo}) para {len(noticias)} noticias...'
    })

@app.route('/api/open-folder', methods=['POST'])
def open_folder():
    """Abrir la carpeta de videos en el explorador de Windows"""
    try:
        VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        os.startfile(str(VIDEOS_DIR))
        return jsonify({'status': 'success', 'path': str(VIDEOS_DIR)})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/videos-list', methods=['GET'])
def videos_list():
    """Listar archivos generados en la carpeta de videos"""
    try:
        VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        archivos = []
        for f in sorted(VIDEOS_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
            if f.is_file():
                archivos.append({
                    'nombre': f.name,
                    'tamaño_mb': round(f.stat().st_size / (1024 * 1024), 2),
                    'tipo': 'video' if f.suffix == '.mp4' else 'documento' if f.suffix == '.docx' else 'otro',
                })
        return jsonify({'archivos': archivos, 'carpeta': str(VIDEOS_DIR)})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/videos/<path:filename>')
def serve_video(filename):
    """Servir un video generado para previsualizarlo en la PWA"""
    return send_from_directory(str(VIDEOS_DIR), filename)

@app.route('/api/state', methods=['GET'])
def get_state():
    """Obtener estado actual del sistema"""
    return jsonify(state)

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    """Verificar que todos los requisitos estén disponibles y auto-reparar"""
    health_agent = HealthCheckAgent()
    resultado = health_agent.verificar_todo(auto_repair=True)

    if resultado['todo_ok']:
        mensaje = '✅ Sistema listo'
        if resultado.get('reparaciones'):
            mensaje += f" (Reparados: {', '.join(resultado['reparaciones'])})"

        return jsonify({
            'status': 'ok',
            'mensaje': mensaje,
            'resultados': resultado['resultados'],
            'reparaciones': resultado.get('reparaciones', [])
        })
    else:
        return jsonify({
            'status': 'error',
            'mensaje': '❌ Faltan requisitos - intenta reparar o instala manualmente',
            'resultados': resultado['resultados'],
            'reparaciones': resultado.get('reparaciones', [])
        }), 400

@app.route('/api/workflow-next', methods=['POST'])
def workflow_next():
    """Avanzar a la siguiente fase en el workflow"""
    data = request.json
    current_phase = data.get('current_phase', 0)

    # Mapeo de fases: qué hacer para avanzar a la siguiente
    next_actions = {
        0: ('Inicializar', '/api/init'),
        1: ('Seleccionar Noticias', 'fase1-select'),
        2: ('Ejecutar Fase 2', '/api/phase2'),
        2.5: ('Revisar Ideas', 'fase2-correct'),
        3: ('Ejecutar Fase 3', '/api/phase3'),
        3.5: ('Revisar Captions', 'fase3-correct'),
        4: ('Ejecutar Fase 4', '/api/phase4'),
    }

    return jsonify({
        'status': 'ok',
        'current_phase': current_phase,
        'next_phase': current_phase + 1,
        'message': f'Listo para siguiente fase'
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset del sistema"""
    global state
    state = {
        'status': 'idle',
        'current_phase': 0,
        'noticias': [],
        'noticias_indices_seleccionadas': [],
        'noticia_seleccionada': None,
        'ideas': [],
        'ideas_seleccionadas': [],
        'prompts': [],
        'captions': [],
        'captions_seleccionados': [],
        'video': None,
        'error': None,
        'timestamp': None,
        'progress': {
            'activo': False,
            'porcentaje': 0,
            'paso': '',
            'detalle': '',
            'logs': [],
        },
        'resultado_final': None,
    }
    return jsonify({'status': 'success'})

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/composite-image', methods=['POST'])
def composite_image():
    """Recibir imagen meme + componer El Típico Canario en posición elegida"""
    if not orquestador:
        return jsonify({'status': 'error', 'error': 'Orquestador no inicializado'}), 400

    try:
        # Verificar archivo
        if 'imagen' not in request.files:
            return jsonify({'status': 'error', 'error': 'No se envió imagen'}), 400

        archivo = request.files['imagen']
        if archivo.filename == '':
            return jsonify({'status': 'error', 'error': 'Archivo vacío'}), 400

        # Parámetros opcionales
        posicion = request.form.get('posicion', 'derecha')
        escala = float(request.form.get('escala', 0.45))

        # Validar parámetros
        if posicion not in ['izquierda', 'derecha', 'centro', 'arriba', 'abajo']:
            posicion = 'derecha'
        if escala < 0.2 or escala > 0.8:
            escala = 0.45

        # Guardar archivo temporalmente
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            archivo.save(tmp.name)
            tmp_path = tmp.name

        try:
            # Componer imagen
            resultado = orquestador.image_compositor.ejecutar(
                imagen_path=tmp_path,
                posicion=posicion,
                escala=escala
            )

            if resultado.get('status') != 'success':
                return jsonify({
                    'status': 'error',
                    'error': resultado.get('error', 'Error desconocido')
                }), 400

            # Devolver info de la imagen generada
            return jsonify({
                'status': 'success',
                'imagen_filename': resultado.get('imagen_filename'),
                'imagen_path': resultado.get('imagen_path'),
                'posicion': posicion,
                'escala': escala,
                'mensaje': f'Imagen compuesta con El Típico ({posicion})'
            })

        finally:
            # Limpiar temporal
            try:
                os.unlink(tmp_path)
            except:
                pass

    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  AJAMSI - Backend API")
    print("  Servidor en http://localhost:5000")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
