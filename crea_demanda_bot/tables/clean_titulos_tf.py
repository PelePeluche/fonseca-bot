import pandas as pd
import re

def clean_data(input_path, output_path):
    print(f"Loading file: {input_path}")
    try:
        df = pd.read_excel(input_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # 1. Clean CUIT: Remove non-digits
    print("Cleaning 'CUIT' column...")
    if 'CUIT' in df.columns:
        # Convert to string, replace non-digits with empty string
        df['CUIT'] = df['CUIT'].astype(str).apply(lambda x: re.sub(r'\D', '', x))
    else:
        print("WARNING: 'CUIT' column not found!")

    # 2. Add 'Tipo de Persona'
    print("Classifying 'Tipo de Persona'...")
    def classify_persona(cuit):
        if not cuit: 
            return "Desconocido"
        prefix = cuit[:2]
        if prefix in ['20', '23', '24', '27']:
            return "Fisica"
        elif prefix in ['30', '33', '34']:
            return "Juridica"
        else:
            return "Desconocido"

    df['Tipo de Persona'] = df['CUIT'].apply(classify_persona)
    
    # 3. Update 'Repartición'
    print("Updating 'Repartición' column...")
    if 'Repartición' in df.columns:
        # Replace specific value "TF" with "Tribunal de falta"
        # We use strict replacement or regex=False to avoid partial matches if "TF" is part of another word
        df['Repartición'] = df['Repartición'].replace('TF', 'Tribunal de falta')
        
        # If the user meant *fill* all rows, or just replace TF? 
        # Requirement: "en Repartición, cambién TF por Tribunal de falta" -> Implies replacement.
    else:
        print("WARNING: 'Repartición' column not found!")

    # Save output
    print(f"Saving cleaned data to: {output_path}")
    df.to_excel(output_path, index=False)
    print("Done.")

if __name__ == "__main__":
    input_file = "/home/peluche/Escritorio/Ramiro Bot/fonseca-bot/crea_demanda_bot/tables/Títulos TF (20-12-2025).xlsx"
    # Overwrite the file as preferred by user ("cambios sobre esta tabla")
    output_file = "/home/peluche/Escritorio/Ramiro Bot/fonseca-bot/crea_demanda_bot/tables/Títulos TF (20-12-2025).xlsx"
    
    clean_data(input_file, output_file)
