import sys
import os
from cryptography.fernet import Fernet
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from SERVICIOS.api_service import PostService

# Asegurando que la carpeta raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Configuración de la app Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Base de datos local
db = SQLAlchemy(app)

# Función para generar la clave (solo ejecutar una vez)
def generar_clave():
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(clave)

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

@app.route('/posts', methods=['GET'])
def obtener_posts():
    posts = PostService.obtener_posts()
    if posts:
        posts_list = [{"id": post.id, "title": post.title, "body": post.body} for post in posts]
        return jsonify(posts_list), 200
    else:
        return jsonify({"message": "No posts found"}), 404

# Ruta para encriptar y desencriptar una cadena
@app.route('/encriptar', methods=['POST'])
def encriptar_y_desencriptar():
    try:
        cadena_original = "Este es un texto que se va a encriptar"
        print(f"Texto original: {cadena_original}")
        
        # Encriptar la cadena
        cadena_encriptada = encriptar_cadena(cadena_original)
        print(f"\nCadena encriptada: {cadena_encriptada}")
        
        # Desencriptar la cadena
        cadena_desencriptada = desencriptar_cadena(cadena_encriptada)
        print(f"Cadena desencriptada: {cadena_desencriptada}")

        # Devolver la respuesta con la información de encriptación
        return jsonify({
            "cadena_original": cadena_original,
            "cadena_encriptada": cadena_encriptada.decode(),
            "cadena_desencriptada": cadena_desencriptada
        }), 200
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return jsonify({"error": "Ha ocurrido un error"}), 500

if __name__ == '__main__':
    app.run(debug=True)