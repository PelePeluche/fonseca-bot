# File: verify_file.py

import os

def verify_file(file_path):
    if os.path.exists(file_path):
        print("El archivo existe en la ruta especificada.")
    else:
        print("El archivo NO existe en la ruta especificada.")
        return False
    return True
