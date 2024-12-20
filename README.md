# Proyecto POO - Encriptación, API y Solicitudes HTTP

Este proyecto implementa procesos clave de Programación Orientada a Objetos (POO) utilizando Flask, MySQL y SQLAlchemy.

## Funcionalidades
Encriptación de Contraseña: Encripta y verifica contraseñas con Fernet y bcrypt.
Obtención de Datos: Realiza solicitudes GET a la API jsonplaceholder y almacena datos en MySQL.
Envío de Datos: Crea objetos mediante solicitudes POST a la API jsonplaceholder.

## Requisitos

**Python 3.9+
**MySQL Server (con XAMPP)

## Bibliotecas
Instalar las dependencias utilizando pip:

pip install flask flask-sqlalchemy cryptography requests pymysql bcrypt

## Base de Datos

** Crear la base de datos evaluacion3:

** CREATE DATABASE evaluacion3;

Archivo clave.key: Generar con el siguiente código:

from cryptography.fernet import Fernet
with open("clave.key", "wb") as f:
    f.write(Fernet.generate_key())

Clonar el repositorio:

git clone https://github.com/tu-usuario/proyecto-poo.git
cd proyecto-poo

Configurar el archivo AUXILIARES/config.py para la conexión con MySQL.

Iniciar la aplicación:

python main.py

Rutas
Inicio: /
Posts: /posts
Encriptación: /encriptar
