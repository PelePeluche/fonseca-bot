import pandas as pd
from typing import List, Dict

OBS_COL = "observaciones"

class ExcelUpdater:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df = pd.read_excel(excel_path)
        if OBS_COL not in self.df.columns:
            self.df[OBS_COL] = None  # Agrega la columna si no existe

    def get_pending_rows(self) -> List[Dict]:
        """
        Devuelve las filas pendientes (no completadas) como lista de dicts.
        """
        pending = self.df[self.df[OBS_COL].isna() | (self.df[OBS_COL] != "completado")]
        return pending.to_dict(orient='records')

    def mark_completed(self, row_idx: int, msg: str = "completado"):
        self.df.at[row_idx, OBS_COL] = msg
        self.df.to_excel(self.excel_path, index=False)

    def reload(self):
        self.df = pd.read_excel(self.excel_path)
