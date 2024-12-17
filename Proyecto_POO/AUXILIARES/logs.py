# logs.py

import logging

def configurar_logs():
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Muestra los logs en la consola
            logging.FileHandler("app.log")  # Guarda los logs en un archivo
        ]
    )

def log_info(message):
    """Registra un mensaje informativo"""
    logging.info(message)

def log_error(message):
    """Registra un mensaje de error"""
    logging.error(message)

def log_warning(message):
    """Registra un mensaje de advertencia"""
    logging.warning(message)