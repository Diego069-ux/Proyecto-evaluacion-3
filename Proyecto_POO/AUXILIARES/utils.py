# utils.py

import re

def validar_email(email):
    """Valida que el email tenga un formato correcto"""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    else:
        return False

def convertir_a_json(data):
    """Convierte datos a formato JSON"""
    import json
    return json.dumps(data)