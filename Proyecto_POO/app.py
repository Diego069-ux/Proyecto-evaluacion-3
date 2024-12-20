import sys
import os
from cryptography.fernet import Fernet
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from SERVICIOS.api_service import PostService

# Asegurando que la carpeta raíz esté en el path
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
    clave = cargar_clave()  # Cargar la clave desde el archivo
    fernet = Fernet(clave)
    return fernet.encrypt(cadena.encode())

# Función para desencriptar una cadena
def desencriptar_cadena(cadena_encriptada):
    clave = cargar_clave()  # Cargar la clave desde el archivo
    fernet = Fernet(clave)
    return fernet.decrypt(cadena_encriptada).decode()

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
        with app.app_context():  # Asegurando el contexto de la app aquí
            posts = PostService.obtener_posts()  # Llama al servicio para obtener los posts
            if posts:
                posts_list = [{"id": post.id, "title": post.title, "body": post.body} for post in posts]
                print(f"Posts encontrados: {posts_list}")  # Depuración en la consola
                return jsonify(posts_list), 200
            else:
                print("No se encontraron posts")  # Depuración en la consola
                return jsonify({"message": "No posts found"}), 404
    except Exception as e:
        print(f"Error obteniendo posts: {e}")  # Depuración en caso de error
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
        # Si la solicitud es POST, procesamos el formulario
        cadena_original = request.form['cadena']
        print(f"Texto original: {cadena_original}")
        
        # Encriptar la cadena
        cadena_encriptada = encriptar_cadena(cadena_original)
        print(f"\nCadena encriptada: {cadena_encriptada}")
        
        # Desencriptar la cadena
        cadena_desencriptada = desencriptar_cadena(cadena_encriptada)
        print(f"Cadena desencriptada: {cadena_desencriptada}")

        return """
        <h1>Resultado de Encriptación y Desencriptación</h1>
        <p><strong>Texto original:</strong> {}</p>
        <p><strong>Cadena encriptada:</strong> {}</p>
        <p><strong>Cadena desencriptada:</strong> {}</p>
        <br>
        <a href="/encriptacion">Volver a probar</a>
        """.format(cadena_original, cadena_encriptada.decode(), cadena_desencriptada)
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return jsonify({"error": f"Ha ocurrido un error: {str(e)}"}), 500

if __name__ == '__main__':
    with app.app_context():  # Garantizar que el contexto de la app esté activo
        try:
            db.engine.connect()  # Intenta realizar una conexión con la base de datos
            print("Conexión exitosa a la base de datos.")
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")

        # Crear tablas si no existen
        db.create_all()

    # Ejecutar la aplicación Flask
    app.run(debug=True)
