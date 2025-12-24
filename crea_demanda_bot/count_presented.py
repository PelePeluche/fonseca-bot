import os
import pandas as pd

# Lista de rutas de archivos Excel
file_paths = [
    'crea_demanda_bot/tables/Sonzini - Iniciar demanda - 2024 (parte 2).xlsx',
]

# Función para contar filas con y sin presentación en la columna 'Presentación'
def count_rows_with_and_without_presentation(file_path):
    # Cargamos el archivo Excel
    data = pd.read_excel(file_path)
    
    # Total de filas
    total_rows = len(data)
    
    # Filas con un valor en la columna 'Presentación'
    rows_with_presentation = data['Presentación'].notnull().sum()
    
    # Filas sin un valor en la columna 'Presentación'
    rows_without_presentation = total_rows - rows_with_presentation
    
    return total_rows, rows_with_presentation, rows_without_presentation

# Inicializamos los contadores globales
total_demandas = 0
total_presentadas = 0
total_no_presentadas = 0

# Procesamos cada archivo
for file_path in file_paths:
    file_name = os.path.basename(file_path)
    try:
        total_rows, rows_with_presentation, rows_without_presentation = count_rows_with_and_without_presentation(file_path)
        
        # Sumamos al total general
        total_demandas += total_rows
        total_presentadas += rows_with_presentation
        total_no_presentadas += rows_without_presentation
        
        # Calculamos los porcentajes para este archivo
        percent_presentadas = (rows_with_presentation / total_rows) * 100 if total_rows > 0 else 0
        percent_no_presentadas = (rows_without_presentation / total_rows) * 100 if total_rows > 0 else 0
        
        # Mostramos resultados para cada archivo
        print(f"Archivo: {file_name}")
        print(f"Total de demandas: {total_rows}")
        print(f"Demandas presentadas: {rows_with_presentation} ({percent_presentadas:.2f}%)")
        print(f"Demandas no presentadas: {rows_without_presentation} ({percent_no_presentadas:.2f}%)")
        print("\n")
    
    except Exception as e:
        print(f"Error procesando el archivo {file_name}: {str(e)}")

# Calculamos los porcentajes totales
percent_total_presentadas = (total_presentadas / total_demandas) * 100 if total_demandas > 0 else 0
percent_total_no_presentadas = (total_no_presentadas / total_demandas) * 100 if total_demandas > 0 else 0

# Mostramos los resultados totales
print(f"Total de demandas en todos los archivos: {total_demandas}")
print(f"Total de demandas presentadas en todos los archivos: {total_presentadas} ({percent_total_presentadas:.2f}%)")
print(f"Total de demandas no presentadas en todos los archivos: {total_no_presentadas} ({percent_total_no_presentadas:.2f}%)")
