import requests
import json
import pandas as pd
from config import cookies

# Función para obtener todas las presentaciones (99999) desde la API
def obtener_presentaciones():
    url = "https://www.justiciacordoba.gob.ar/PresentacionDemandas/Presentaciones/PresentacionSorteadasLista.aspx/MisPresentaciones"
    headers = {
        "Origin": "https://www.justiciacordoba.gob.ar",
        "Referer": "https://www.justiciacordoba.gob.ar/PresentacionDemandas/Presentaciones/PresentacionSorteadasLista.aspx",
        "Content-Type": "application/json",
        "Cookie": cookies,
    }
    data = {"pageSize": 99999, "pageIndex": 0}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(response.json())
        return response.json()["d"]["ReturnData"]
    else:
        print(f"Error en la solicitud. Código de estado: {response.status_code}")
        return []


# Función para machear la tabla del Excel con los datos obtenidos de la API
def machear_con_presentaciones(df, presentaciones):
    df["IdReference"] = ""  # Nueva columna para almacenar IdReference o Not found

    for index, row in df.iterrows():
        presentacion = row.get("Presentación")
        if pd.notna(presentacion):  # Si la presentación no es NaN
            # Buscar el Id correspondiente en la lista de presentaciones
            matched = next(
                (p for p in presentaciones if p["Id"] == int(presentacion)), None
            )
            if matched:
                df.at[index, "IdReference"] = matched["IdReference"]
            else:
                df.at[index, "IdReference"] = "Not found"
        else:
            df.at[index, "IdReference"] = "Not found"

    return df


def main():
    # Cargar el archivo Excel
    excel_path = "crea_demanda_bot/tables/NOT FOUND PARA INICIAR TF RAMIRO SONZINI.xlsx"
    df = pd.read_excel(excel_path)

    # Obtener los datos de presentaciones desde la API con las cookies extraídas
    presentaciones = obtener_presentaciones()

    # Machear la tabla con las presentaciones
    df_macheada = machear_con_presentaciones(df, presentaciones)

    # Guardar el nuevo archivo Excel con la columna IdReference
    df_macheada.to_excel("crea_demanda_bot/tables/NOT FOUND PARA INICIAR TF RAMIRO SONZINI con IdReference.xlsx", index=False)
    print("Archivo con IdReference creado exitosamente: archivo_macheado.xlsx")


if __name__ == "__main__":
    main()
