# conexion_db.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AUXILIARES')))

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
        try:
            conexion = pymysql.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG.get("password", ""), 
                db=DB_CONFIG["database"]
            )
            print("Conexión exitosa a la base de datos.")
            return conexion
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
