import pandas as pd
from typing import List, Dict

def read_excel_as_dicts(excel_path: str, sheet_name: str = 0) -> List[Dict]:
    """
    Lee un archivo Excel y devuelve una lista de diccionarios, uno por cada fila.
    Cada diccionario tiene como claves los nombres de las columnas.
    """
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    # Elimina filas completamente vacías
    df = df.dropna(how='all')
    # Convierte a lista de diccionarios
    return df.to_dict(orient='records')
