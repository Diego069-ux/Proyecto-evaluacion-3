# conexion_db.py

import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AUXILIARES')))

# Verifica si la carpeta AUXILIARES está en el sys.path
print(sys.path)

from config import DB_CONFIG

# Verifica que DB_CONFIG fue importado correctamente
print(DB_CONFIG)

import pymysql

class DBManager:
    @staticmethod
    def obtener_conexion():
        """
        Crea y devuelve una conexión a la base de datos MySQL utilizando la configuración de config.py.
        """
        return pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG.get("password", ""), 
            db=DB_CONFIG["database"]
        )
