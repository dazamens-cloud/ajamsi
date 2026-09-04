"""
AJAMSI - Backend API Flask
API para ejecutar el pipeline de manera interactiva
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
from pathlib import Path
import json
import threading
from datetime import datetime

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
}

orquestador = None

@app.route('/')
def index():
    """Sirve la interfaz web"""
    try:
        html_path = Path(__file__).parent / 'app_frontend.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        return f"<h1>Error cargando HTML: {e}</h1>", 500

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

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset del sistema"""
    global state
    state = {
        'status': 'idle',
        'current_phase': 0,
        'noticias': [],
        'noticia_seleccionada': None,
        'ideas': [],
        'prompts': [],
        'captions': [],
        'video': None,
        'error': None,
        'timestamp': None,
    }
    return jsonify({'status': 'success'})

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  AJAMSI - Backend API")
    print("  Servidor en http://localhost:5000")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
