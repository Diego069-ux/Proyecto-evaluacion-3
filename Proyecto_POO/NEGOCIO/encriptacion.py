# NEGOCIO/encriptacion.py

import bcrypt

class Encriptador:
    @staticmethod
    def encriptar_contraseña(contraseña: str) -> str:
        """Encripta la contraseña con bcrypt"""
        # Genera un salt (un valor aleatorio único)
        salt = bcrypt.gensalt()
        # Encripta la contraseña usando el salt
        contrasena_encriptada = bcrypt.hashpw(contraseña.encode(), salt)
        return contrasena_encriptada.decode()

    @staticmethod
    def verificar_contraseña(contraseña: str, contraseña_encriptada: str) -> bool:
        """Verifica si la contraseña ingresada coincide con la encriptada"""
        return bcrypt.checkpw(contraseña.encode(), contraseña_encriptada.encode())