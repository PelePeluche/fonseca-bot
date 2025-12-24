import pandas as pd
import os


def save_rows_in_range(input_file, output_file, start_row, end_row):
    # Leer el archivo Excel
    data = pd.read_excel(input_file)

    # Verificar si el rango es válido
    if start_row < 0 or end_row > len(data):
        print("Rango fuera de los límites.")
        return

    # Filtrar las filas en el rango especificado
    filtered_data = data.iloc[start_row:end_row]

    # Guardar el nuevo archivo Excel con las filas filtradas
    filtered_data.to_excel(output_file, index=False)
    print(f"Archivo guardado con éxito en: {output_file}")


# Ejemplo de uso
input_file = (
    "crea_demanda_bot/tables/Merged_Tables_Specific_Fields.xlsx"
)
output_file = (
    "crea_demanda_bot/tables/Merged_Tables_Specific_Fields_2.xlsx"
)
start_row = 600
end_row = 803

save_rows_in_range(input_file, output_file, start_row, end_row)
