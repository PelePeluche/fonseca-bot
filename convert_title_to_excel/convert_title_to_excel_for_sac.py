import os
import pandas as pd

# Ruta de la carpeta con los títulos (PDFs)
titles_folder = '/home/fernando/Escritorio/Ramiro Bot/fonseca-bot/titles/Pedir CNOE (parte 2)/'
output_excel = 'titles_for_sac.xlsx'

data = []

for filename in os.listdir(titles_folder):
    if filename.lower().endswith('.pdf'):
        idsac = os.path.splitext(filename)[0]
        data.append({
            'IdSAC': idsac,
            'Archivo': filename
        })

# Crear DataFrame y guardar Excel
if data:
    df = pd.DataFrame(data)
    df.to_excel(output_excel, index=False)
    print(f"Archivo Excel generado exitosamente: {output_excel}")
else:
    print("No se encontraron archivos PDF en la carpeta indicada.")
