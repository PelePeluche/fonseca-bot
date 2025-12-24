import os
import pandas as pd

# Directorio donde están los archivos
folder_path = 'crea_demanda_bot/tables'

# Crear una lista vacía para almacenar los dataframes
dataframes = []

# Iterar sobre los archivos en el directorio
for file_name in os.listdir(folder_path):
    if file_name.startswith("Merged") and file_name.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file_name)
        try:
            # Leer el archivo Excel y agregar el dataframe a la lista
            df = pd.read_excel(file_path)
            dataframes.append(df)
            print(f"Archivo {file_name} procesado.")
        except Exception as e:
            print(f"Error al procesar el archivo {file_name}: {str(e)}")

# Concatenar todos los dataframes
combined_df = pd.concat(dataframes, ignore_index=True)

# Guardar el resultado en un nuevo archivo Excel
output_file = os.path.join(folder_path, 'Fonseca - Iniciar demanda - 2024 (parte 2).xlsx')
combined_df.to_excel(output_file, index=False)

print(f"Todos los archivos se han combinado en {output_file}")
