import bcrypt
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from requests.auth import HTTPBasicAuth

# Inicializar la app de Flask
app = Flask(__name__)

# Configuración de la base de datos MySQL con SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:contraseña@localhost/mi_basededatos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Modelo Post (corresponde a la tabla 'posts' en la base de datos)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)

# Ruta para encriptar y desencriptar contraseñas
@app.route('/encriptar', methods=['POST'])
def encriptar_contraseña():
    # Solicitar al usuario la contraseña
    password = request.json.get('password')
    print(f'Contraseña ingresada: {password}')
    
    # Encriptar la contraseña
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(f'Contraseña encriptada: {hashed}')
    
    # Desencriptar y comparar
    if bcrypt.checkpw(password.encode('utf-8'), hashed):
        print('La contraseña coincide con la original.')
    else:
        print('La contraseña no coincide.')
    
    return jsonify({'mensaje': 'Proceso de encriptación y desencriptación completado'})

# Ruta para obtener los datos desde la API y almacenarlos en la base de datos
@app.route('/obtener-datos', methods=['GET'])
def obtener_datos():
    # Hacer una solicitud GET a la API de jsonplaceholder
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    
    if response.status_code == 200:
        # Almacenar los datos en la base de datos
        posts_data = response.json()
        
        for post_data in posts_data:
            nuevo_post = Post(title=post_data['title'], body=post_data['body'])
            db.session.add(nuevo_post)
        
        db.session.commit()
        
        # Consultar los datos de la base de datos
        posts = Post.query.all()
        posts_list = [{'id': post.id, 'title': post.title, 'body': post.body} for post in posts]
        
        return jsonify(posts_list), 200
    else:
        return jsonify({'mensaje': 'Error al obtener los datos de la API'}), 500

# Ruta para hacer un envío de data mediante POST a la API
@app.route('/enviar-datos', methods=['POST'])
def enviar_datos():
    # Solicitar datos al usuario para crear un objeto
    title = request.json.get('title')
    body = request.json.get('body')
    
    # Crear el objeto en la API
    payload = {'title': title, 'body': body, 'userId': 1}
    response = requests.post('https://jsonplaceholder.typicode.com/posts', json=payload)
    
    if response.status_code == 201:
        return jsonify({'mensaje': 'Objeto creado correctamente en la API'}), 200
    else:
        return jsonify({'mensaje': 'Error al crear el objeto en la API'}), 500

# Ruta para hacer una solicitud HTTP con autenticación a la API Serper
@app.route('/buscar-google', methods=['POST'])
def buscar_google():
    # Solicitar al usuario el string de búsqueda
    query = request.json.get('query')
    api_key = 'tu_api_key'  # Sustituir con tu clave de API de Serper
    
    # Realizar la solicitud GET con autenticación
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(f'https://api.serper.dev/search?q={query}', headers=headers)
    
    if response.status_code == 200:
        results = response.json()
        return jsonify(results), 200
    else:
        return