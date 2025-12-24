import pandas as pd
import os

def merge_files(base_path, titles_path, output_path):
    print(f"Loading Base File: {base_path}")
    try:
        df_base = pd.read_excel(base_path)
    except Exception as e:
        print(f"Error loading base file: {e}")
        return

    print(f"Loading Titles File: {titles_path}")
    try:
        df_titles = pd.read_excel(titles_path)
    except Exception as e:
        print(f"Error loading titles file: {e}")
        return

    print(f"Rows in Base: {len(df_base)}")
    print(f"Rows in Titles: {len(df_titles)}")

    # Clean and Standardize 'Causa' columns
    print("Normalizing 'Causa' columns...")
    
    # Base File: Convert to numeric, handle potential non-numeric garbage, drop NaNs, convert to int, then string
    df_base['Causa_Clean'] = pd.to_numeric(df_base['Causa'], errors='coerce')
    original_len_base = len(df_base)
    df_base = df_base.dropna(subset=['Causa_Clean'])
    print(f"Dropped {original_len_base - len(df_base)} rows from Base due to invalid/missing Causa")
    df_base['Causa_Clean'] = df_base['Causa_Clean'].astype(int).astype(str).str.strip()

    # Titles File: Similar process to ensure consistency
    df_titles['Causa_Clean'] = pd.to_numeric(df_titles['Causa Nro.'], errors='coerce')
    original_len_titles = len(df_titles)
    df_titles = df_titles.dropna(subset=['Causa_Clean'])
    print(f"Dropped {original_len_titles - len(df_titles)} rows from Titles due to invalid/missing Causa")
    df_titles['Causa_Clean'] = df_titles['Causa_Clean'].astype(int).astype(str).str.strip()

    # Perform Right Join to keep all records from Titles file
    # 'Causa' from Base, 'Causa Nro.' from Titles
    print("Merging files (Right Join)...")
    merged_df = pd.merge(
        df_base, 
        df_titles, 
        left_on='Causa_Clean', 
        right_on='Causa_Clean', 
        how='right'
    )

    # Drop the temporary joining column if desired, or keep it. 
    # For cleanliness, we drop the duplicate keys and the temp column
    merged_df = merged_df.drop(columns=['Causa_Clean'])

    print(f"Rows in Merged Result: {len(merged_df)}")

    if len(merged_df) == 0:
        print("WARNING: No matches found! Check if the 'Causa' numbers are formatted identically in both files.")
    else:
        merged_df.to_excel(output_path, index=False)
        print(f"Success! Merged file saved to: {output_path}")

if __name__ == "__main__":
    # Paths configuration
    base_file_path = "/home/peluche/Escritorio/Ramiro Bot/fonseca-bot/TF - Iniciar Nov. 2025-20251219T190932Z-3-001/TF - Iniciar Nov. 2025/TF Extra Base FONSECA.xls"
    titles_file_path = "/home/peluche/Escritorio/Ramiro Bot/fonseca-bot/Títulos TF (20-12-2025).xlsx"
    output_file_path = "/home/peluche/Escritorio/Ramiro Bot/fonseca-bot/convert_title_to_excel/TF_Merge_Final.xlsx"

    merge_files(base_file_path, titles_file_path, output_file_path)
