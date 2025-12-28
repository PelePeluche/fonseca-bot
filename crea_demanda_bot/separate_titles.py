import argparse
import os
from pathlib import Path
import string

import pandas as pd


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


def _excel_suffix(index: int) -> str:
    if index < 0:
        raise ValueError("index must be >= 0")
    letters = string.ascii_uppercase
    base = len(letters)
    out = ""
    i = index
    while True:
        i, rem = divmod(i, base)
        out = letters[rem] + out
        if i == 0:
            break
        i -= 1
    return out


def split_excel_in_chunks(input_file: str, chunk_size: int = 500, output_dir: str | None = None):
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    out_dir = Path(output_dir) if output_dir else input_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    data = pd.read_excel(input_path)
    total_rows = len(data)
    if total_rows == 0:
        print("El archivo Excel está vacío.")
        return []

    outputs: list[Path] = []
    chunk_index = 0
    for start in range(0, total_rows, chunk_size):
        end = min(start + chunk_size, total_rows)
        suffix = _excel_suffix(chunk_index)
        out_path = out_dir / f"{input_path.stem}_{suffix}{input_path.suffix}"
        data.iloc[start:end].to_excel(out_path, index=False)
        print(f"Archivo guardado con éxito en: {out_path} ({end - start} filas)")
        outputs.append(out_path)
        chunk_index += 1

    return outputs


# Ejemplo de uso
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    split_excel_in_chunks(args.input, chunk_size=args.chunk_size, output_dir=args.output_dir)
