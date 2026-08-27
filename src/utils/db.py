"""
Manejo de base de datos SQLite para AjamSi
"""

import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gestor de base de datos SQLite"""

    def __init__(self, config_or_path: Union[Dict, str, Path]):
        """
        Inicializar gestor de base de datos

        Args:
            config_or_path: Configuración dict o ruta al archivo de base de datos
        """
        # Extraer db_path de config si es necesario
        if isinstance(config_or_path, dict):
            db_file = config_or_path.get("base_datos", {}).get("archivo", "data/ajamsi.db")
            self.db_path = Path(db_file)
        else:
            self.db_path = Path(config_or_path)

        # Crear directorio si no existe
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = None
        self.initialize()

    def initialize(self):
        """Inicializar la base de datos y crear tablas si no existen"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()

        # Tabla de noticias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS noticias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                fuente TEXT NOT NULL,
                contenido TEXT,
                fecha_publicacion DATETIME,
                fecha_scrapeado DATETIME DEFAULT CURRENT_TIMESTAMP,
                relevancia_score FLOAT DEFAULT 0.0,
                usado INTEGER DEFAULT 0,
                fecha_usado DATETIME
            )
        ''')

        # Tabla de ideas generadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                noticia_id INTEGER NOT NULL,
                concepto TEXT NOT NULL,
                angulo_humor TEXT,
                estado TEXT DEFAULT 'pendiente',
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                feedback TEXT,
                FOREIGN KEY (noticia_id) REFERENCES noticias(id)
            )
        ''')

        # Tabla de imágenes generadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imagenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id INTEGER NOT NULL,
                ruta_archivo TEXT NOT NULL,
                prompt_usado TEXT,
                proveedor TEXT DEFAULT 'gemini',
                fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                feedback TEXT,
                estado TEXT DEFAULT 'completado',
                FOREIGN KEY (idea_id) REFERENCES ideas(id)
            )
        ''')

        # Tabla de videos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imagen_id INTEGER NOT NULL,
                idea_id INTEGER NOT NULL,
                ruta_archivo TEXT NOT NULL,
                guion TEXT,
                duracion_segundos FLOAT,
                fecha_compilacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                feedback TEXT,
                estado TEXT DEFAULT 'compilado',
                subido_tiktok INTEGER DEFAULT 0,
                FOREIGN KEY (imagen_id) REFERENCES imagenes(id),
                FOREIGN KEY (idea_id) REFERENCES ideas(id)
            )
        ''')

        # Tabla de feedback
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                idea_id INTEGER,
                imagen_id INTEGER,
                tipo_feedback TEXT NOT NULL,
                comentario TEXT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(id),
                FOREIGN KEY (idea_id) REFERENCES ideas(id),
                FOREIGN KEY (imagen_id) REFERENCES imagenes(id)
            )
        ''')

        self.connection.commit()
        print("✓ Base de datos inicializada correctamente")

    def insertar_noticia(self, titulo: str, url: str, fuente: str, contenido: str, fecha_pub: datetime = None) -> int:
        """Insertar noticia en la base de datos"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO noticias (titulo, url, fuente, contenido, fecha_publicacion)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, url, fuente, contenido, fecha_pub or datetime.now()))
        self.connection.commit()
        return cursor.lastrowid

    def obtener_noticias_sin_usar(self, limite: int = 10) -> List[Dict]:
        """Obtener noticias que no han sido usadas aún"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM noticias
            WHERE usado = 0
            ORDER BY fecha_publicacion DESC
            LIMIT ?
        ''', (limite,))
        return [dict(row) for row in cursor.fetchall()]

    def insertar_idea(self, noticia_id: int, concepto: str, angulo_humor: str = None) -> int:
        """Insertar idea generada"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO ideas (noticia_id, concepto, angulo_humor)
            VALUES (?, ?, ?)
        ''', (noticia_id, concepto, angulo_humor))
        self.connection.commit()
        return cursor.lastrowid

    def insertar_imagen(self, idea_id: int, ruta_archivo: str, prompt: str, proveedor: str = 'gemini') -> int:
        """Insertar imagen generada"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO imagenes (idea_id, ruta_archivo, prompt_usado, proveedor)
            VALUES (?, ?, ?, ?)
        ''', (idea_id, ruta_archivo, prompt, proveedor))
        self.connection.commit()
        return cursor.lastrowid

    def insertar_video(self, imagen_id: int, idea_id: int, ruta_archivo: str, guion: str, duracion: float) -> int:
        """Insertar video compilado"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO videos (imagen_id, idea_id, ruta_archivo, guion, duracion_segundos)
            VALUES (?, ?, ?, ?, ?)
        ''', (imagen_id, idea_id, ruta_archivo, guion, duracion))
        self.connection.commit()
        return cursor.lastrowid

    def insertar_feedback(self, tipo_feedback: str, video_id: int = None, idea_id: int = None,
                         imagen_id: int = None, comentario: str = None):
        """Registrar feedback del usuario"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO feedback_log (video_id, idea_id, imagen_id, tipo_feedback, comentario)
            VALUES (?, ?, ?, ?, ?)
        ''', (video_id, idea_id, imagen_id, tipo_feedback, comentario))
        self.connection.commit()

    def obtener_stats(self) -> Dict:
        """Obtener estadísticas de la base de datos"""
        cursor = self.connection.cursor()

        stats = {}

        cursor.execute('SELECT COUNT(*) FROM noticias')
        stats['total_noticias'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM ideas')
        stats['total_ideas'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM imagenes')
        stats['total_imagenes'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM videos')
        stats['total_videos'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM noticias WHERE usado = 1')
        stats['noticias_usadas'] = cursor.fetchone()[0]

        return stats

    def guardar_noticia(self, noticia) -> Optional[int]:
        """
        Guardar objeto Noticia en la base de datos

        Args:
            noticia: Objeto Noticia (dataclass)

        Returns:
            ID de la noticia insertada o None si error
        """
        try:
            return self.insertar_noticia(
                titulo=noticia.titulo,
                url=noticia.url,
                fuente=noticia.fuente,
                contenido=noticia.contenido,
                fecha_pub=noticia.fecha_publicacion
            )
        except Exception as e:
            logger.error(f"Error guardando noticia: {e}")
            return None

    def guardar_idea(self, idea) -> Optional[int]:
        """
        Guardar objeto Idea en la base de datos

        Args:
            idea: Objeto Idea (dataclass)

        Returns:
            ID de la idea insertada o None si error
        """
        try:
            return self.insertar_idea(
                noticia_id=idea.noticia_id or 1,  # Fallback si no hay noticia_id
                concepto=idea.concepto,
                angulo_humor=idea.angulo_humor
            )
        except Exception as e:
            logger.error(f"Error guardando idea: {e}")
            return None

    def guardar_video(self, video) -> Optional[int]:
        """
        Guardar objeto Video en la base de datos

        Args:
            video: Objeto Video (dataclass)

        Returns:
            ID del video insertado o None si error
        """
        try:
            return self.insertar_video(
                imagen_id=1,  # Fallback (relacionar con imagen después)
                idea_id=1,    # Fallback (relacionar con idea después)
                ruta_archivo=video.ruta_archivo,
                guion="",     # Sin guion por ahora
                duracion=video.duracion_segundos
            )
        except Exception as e:
            logger.error(f"Error guardando video: {e}")
            return None

    def contar_noticias(self) -> int:
        """Contar total de noticias en la BD"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM noticias')
        return cursor.fetchone()[0]

    def contar_ideas(self) -> int:
        """Contar total de ideas en la BD"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM ideas')
        return cursor.fetchone()[0]

    def contar_imagenes(self) -> int:
        """Contar total de imágenes en la BD"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM imagenes')
        return cursor.fetchone()[0]

    def contar_videos(self) -> int:
        """Contar total de videos en la BD"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM videos')
        return cursor.fetchone()[0]

    def cerrar(self):
        """Cerrar conexión a la base de datos"""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cerrar()
