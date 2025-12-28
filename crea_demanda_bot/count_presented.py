import argparse
from pathlib import Path

import pandas as pd


def _is_filled(series: pd.Series) -> pd.Series:
    s = series.astype(str)
    return series.notna() & (s.str.strip() != "") & (s.str.lower() != "nan")


def _select_default_files(tables_dir: Path, letters: list[str]) -> list[Path]:
    pattern = f"*_[{''.join(letters)}].xlsx"
    candidates = list(tables_dir.glob(pattern))

    by_letter: dict[str, list[Path]] = {l: [] for l in letters}
    for p in candidates:
        for l in letters:
            if p.stem.endswith(f"_{l}"):
                by_letter[l].append(p)
                break

    selected: list[Path] = []
    for l in letters:
        if by_letter[l]:
            selected.append(max(by_letter[l], key=lambda x: x.stat().st_mtime))
    return selected


def _count_file(file_path: Path, column: str) -> tuple[int, int, int, str]:
    df = pd.read_excel(file_path, dtype=object)
    total_rows = int(len(df))
    if column not in df.columns:
        return total_rows, 0, total_rows, "SIN_COLUMNA"

    filled = int(_is_filled(df[column]).sum())
    empty = total_rows - filled
    return total_rows, filled, empty, "OK"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tables-dir",
        default=str(Path(__file__).resolve().parent / "tables"),
    )
    parser.add_argument("--column", default="Presentación")
    parser.add_argument("--letters", default="A,B,C,D,E,F")
    parser.add_argument(
        "--files",
        nargs="*",
        default=None,
    )
    args = parser.parse_args(argv)

    letters = [x.strip() for x in args.letters.split(",") if x.strip()]
    tables_dir = Path(args.tables_dir)
    if not tables_dir.exists():
        print(f"No existe: {tables_dir.resolve()}")
        return 2

    if args.files:
        file_paths = [Path(p) for p in args.files]
    else:
        file_paths = _select_default_files(tables_dir, letters)

    if not file_paths:
        print(f"No encontré archivos para procesar en: {tables_dir.resolve()}")
        return 3

    total_demandas = 0
    total_presentadas = 0
    total_no_presentadas = 0

    for file_path in file_paths:
        file_name = file_path.name
        try:
            total_rows, rows_with_presentation, rows_without_presentation, status = _count_file(
                file_path, args.column
            )

            total_demandas += total_rows
            total_presentadas += rows_with_presentation
            total_no_presentadas += rows_without_presentation

            if status == "OK":
                percent_presentadas = (
                    (rows_with_presentation / total_rows) * 100 if total_rows > 0 else 0
                )
                percent_no_presentadas = (
                    (rows_without_presentation / total_rows) * 100 if total_rows > 0 else 0
                )
                print(f"Archivo: {file_name}")
                print(f"Total de demandas: {total_rows}")
                print(
                    f"Demandas presentadas: {rows_with_presentation} ({percent_presentadas:.2f}%)"
                )
                print(
                    f"Demandas no presentadas: {rows_without_presentation} ({percent_no_presentadas:.2f}%)"
                )
                print("\n")
            else:
                print(f"Archivo: {file_name} ({status})")
                print(f"Total de demandas: {total_rows}")
                print("\n")

        except Exception as e:
            print(f"Error procesando el archivo {file_name}: {str(e)}")

    percent_total_presentadas = (
        (total_presentadas / total_demandas) * 100 if total_demandas > 0 else 0
    )
    percent_total_no_presentadas = (
        (total_no_presentadas / total_demandas) * 100 if total_demandas > 0 else 0
    )

    print(f"Total de demandas en todos los archivos: {total_demandas}")
    print(
        f"Total de demandas presentadas en todos los archivos: {total_presentadas} ({percent_total_presentadas:.2f}%)"
    )
    print(
        f"Total de demandas no presentadas en todos los archivos: {total_no_presentadas} ({percent_total_no_presentadas:.2f}%)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
