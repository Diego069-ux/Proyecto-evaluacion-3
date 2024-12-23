import sys
import os
import logging
from cryptography.fernet import Fernet
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

# Configuración de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Configuración de la app Flask para usar MySQL
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/evaluacion3'  # Base de datos MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la instancia de SQLAlchemy
db = SQLAlchemy()

# Se asegura de registrar la aplicación con la instancia de SQLAlchemy
db.init_app(app)

# Función para cargar la clave desde el archivo
def cargar_clave():
    with open("clave.key", "rb") as archivo_clave:
        return archivo_clave.read()

# Función para encriptar una cadena
def encriptar_cadena(cadena):
    clave = cargar_clave()
    fernet = Fernet(clave)
    return fernet.encrypt(cadena.encode())

# Función para desencriptar una cadena
def desencriptar_cadena(cadena_encriptada):
    clave = cargar_clave()
    fernet = Fernet(clave)
    return fernet.decrypt(cadena_encriptada).decode()

# Modelo Post
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

# Modelo Comment
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = db.relationship('Post', back_populates='comments')

# Servicio externo simulado
class ExternalService:
    BASE_URL = 'https://jsonplaceholder.typicode.com/posts'

    @staticmethod
    def obtener_posts():
        try:
            response = requests.get(ExternalService.BASE_URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error al obtener posts externos: {e}")
            return None

# Rutas
@app.route('/')
def inicio():
    return """
    <h1>Bienvenido a la API</h1>
    <p>Para probar las funcionalidades, acceda a las siguientes rutas:</p>
    <ul>
        <li><a href="/posts">/posts</a>: Obtiene una lista de posts.</li>
        <li><a href="/encriptacion">/encriptacion</a>: Encripta y desencripta una cadena (solicitud POST).</li>
    </ul>
    """

@app.route('/posts', methods=['GET'])
def obtener_posts():
    try:
        # Obtener posts desde el servicio externo
        posts = ExternalService.obtener_posts()
        if posts:
            logger.info(f"Posts externos obtenidos: {len(posts)}")
            return jsonify(posts), 200
        else:
            logger.warning("No se encontraron posts externos")
            return jsonify({"message": "No posts found"}), 404
    except Exception as e:
        logger.error(f"Error obteniendo posts: {e}")
        return jsonify({"error": "Error al obtener los posts"}), 500

@app.route('/encriptacion', methods=['GET', 'POST'])
def encriptar_y_desencriptar():
    if request.method == 'GET':
        return """
        <h1>Encriptar y Desencriptar</h1>
        <form method="POST">
            <label for="cadena">Introduce una cadena para encriptar:</label><br>
            <input type="text" id="cadena" name="cadena" required><br><br>
            <input type="submit" value="Enviar">
        </form>
        """
    try:
        cadena_original = request.form['cadena']
        logger.info(f"Texto original: {cadena_original}")
        
        cadena_encriptada = encriptar_cadena(cadena_original)
        logger.info(f"Cadena encriptada: {cadena_encriptada}")
        
        cadena_desencriptada = desencriptar_cadena(cadena_encriptada)
        logger.info(f"Cadena desencriptada: {cadena_desencriptada}")

        return """
        <h1>Resultado de Encriptación y Desencriptación</h1>
        <p><strong>Texto original:</strong> {}</p>
        <p><strong>Cadena encriptada:</strong> {}</p>
        <p><strong>Cadena desencriptada:</strong> {}</p>
        <br>
        <a href="/encriptacion">Volver a probar</a>
        """.format(cadena_original, cadena_encriptada.decode(), cadena_desencriptada)
    except Exception as e:
        logger.error(f"Error en la encriptación/desencriptación: {e}")
        return jsonify({"error": f"Ha ocurrido un error: {str(e)}"}), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            db.engine.connect()
            logger.info("Conexión exitosa a la base de datos.")
        except Exception as e:
            logger.error(f"Error de conexión a la base de datos: {e}")

        db.create_all()

    app.run(debug=True)
