Proyecto POO - Encriptación, API y Solicitudes HTTP
Este proyecto implementa procesos clave de Programación Orientada a Objetos (POO) usando Flask, MySQL, y SQLAlchemy.

Funcionalidades
Encriptación de Contraseña: Encripta y verifica contraseñas con Fernet y bcrypt.
Obtención de Datos: Realiza solicitudes GET a la API jsonplaceholder y almacena datos en MySQL.
Envío de Datos: Crea objetos mediante solicitudes POST a la API jsonplaceholder.
Base de Datos: Manejo de operaciones CRUD con SQLAlchemy.
Requisitos
Software:
Python 3.9+, MySQL Server
Bibliotecas:
Instalar con pip: flask flask-sqlalchemy cryptography requests pymysql bcrypt
Base de Datos:
Crear la base de datos evaluacion3.
sql
Copiar código
CREATE DATABASE evaluacion3;
Archivo clave.key:
Generar con:
python
Copiar código
from cryptography.fernet import Fernet
with open("clave.key", "wb") as f:
    f.write(Fernet.generate_key())
Ejecución
Clonar el repositorio:
bash
Copiar código
git clone https://github.com/tu-usuario/proyecto-poo.git
cd proyecto-poo
Configurar AUXILIARES/config.py para MySQL.
Iniciar la aplicación:
bash
Copiar código
python main.py
Acceder a:
Inicio: /
Posts: /posts
Encriptación: /encriptar
