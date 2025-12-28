import argparse
import os
import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent
sys.path.insert(0, str(base_path))

import pandas as pd
from steps.driver_setup import setup_driver
from steps.user_login import user_login
from steps.manage_tabs import open_new_tab
from steps.click_new_presentation import click_new_presentation
from steps.fill_presentation_data_step import fill_presentation_data_step
from steps.step2_common_parts import step_2_common_parts
from steps.legal_representation import step_legal_representation
from steps.new_case_step import step_new_case
from steps.case_detail import case_detail
from steps.get_presentation_number import get_presentation_number
from steps.finish import finish
from config import users, digital_firmados_iniciar_demanda_filename
import time

def main(excel_filename: str | None = None):
    base_path = Path(__file__).resolve().parent
    filename_path = Path(excel_filename or digital_firmados_iniciar_demanda_filename)

    if filename_path.is_absolute():
        excel_path = filename_path
    else:
        excel_path = base_path / "tables" / filename_path
        if not excel_path.exists():
            repo_root = base_path.parent
            excel_path = repo_root / filename_path

    # Verificamos si el archivo Excel existe
    if not excel_path.exists():
        print("El archivo Excel no se encontró.")
        return

    # Cargamos los datos del Excel
    data = pd.read_excel(excel_path)

    if data.empty:
        print("El archivo Excel está vacío.")
        return

    for index, row in data.iterrows():
        try:
            if pd.notna(row["Presentación"]):
                print(f"Fila {index} ya tiene un número de presentación, saltando...")
                continue
        except KeyError:
            print(KeyError)
            pass

        # Por cada fila en el Excel
        case_number = str(row["Identificador"])  # Se puede ajustar la columna
        archivo = row["Archivo"]

        driver = setup_driver()

        try:
            print(f"Ejecutando el expediente {case_number}...")
            presentation_number = execute_steps(
                driver, row
            )  # Pasamos los datos de la fila al ejecutar los steps

            # Agregamos el número de presentación a la fila actual
            data.at[index, "Presentación"] = presentation_number

            data.to_excel(excel_path, index=False)
            print(f"Archivo Excel actualizado: {excel_path}")

        except Exception as e:
            error_message = f"Ocurrió un error con el expediente {case_number}: {e}"
            print(error_message)
        finally:
            driver.quit()

    # Guardamos el Excel con la nueva columna de número de presentación
    data.to_excel(excel_path, index=False)
    print(f"Archivo Excel actualizado: {excel_path}")


def limpiar_cuit(valor):
    """Convierte el valor a un CUIT válido (str de int) o devuelve '0000000000' si no puede."""
    try:
        return str(int(float(valor)))
    except (ValueError, TypeError):
        return "0000000000"


def execute_steps(driver, row):
    print(row)
    case_data = {
        "Archivo": row["Archivo"],

        "Nombre o Razón Social": row["Nombre o Razón Social"],
        # Llamamos a la función para evitar errores cuando no sea un número
        "CUIT": limpiar_cuit(row["CUIT"]),
        "Repartición": row["Repartición"],
        "Orden": str(row["Orden"]).split(".")[0] if row["Orden"] else None,
        "Año": str(row["Año"]).split(".")[0] if row["Año"] else None,
        "Domicilio": str(row["Domicilio"]).replace("*", "°").replace("?", ""),
        "Monto total": row["Monto total"],
        "Tipo de Persona": row["Tipo de Persona"],
        "Identificador": row["Identificador"],
    }

    user_key = "FONSECA"

    username = users[user_key]["matricula"]
    password = users[user_key]["password"]
    procurador = users[user_key]["procurador"]
    numero_decreto = users[user_key]["numero_decreto"]
    fecha_decreto = users[user_key]["fecha_decreto"]
    municipalidad_keyname_to_search = users[user_key]["municipalidad_keyname_to_search"]
    municipalidad_keyname_to_represent = users[user_key][
        "municipalidad_keyname_to_represent"
    ]

    # Ejecutamos los steps necesarios con el driver
    user_login(driver, username, password)
    time.sleep(0.5)
    open_new_tab(driver)
    time.sleep(0.5)
    click_new_presentation(driver)
    time.sleep(0.5)
    fill_presentation_data_step(driver)
    time.sleep(0.5)
    step_2_common_parts(driver, case_data, municipalidad_keyname_to_search)
    time.sleep(0.5)
    step_legal_representation(driver, procurador, municipalidad_keyname_to_represent)
    time.sleep(0.5)
    step_new_case(driver)
    time.sleep(0.5)
    case_detail(driver, case_data, numero_decreto, fecha_decreto)
    time.sleep(0.5)
    presentation_number = get_presentation_number(driver)
    time.sleep(0.5)
    finish(driver)
    time.sleep(0.5)

    return presentation_number


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", default=None)
    args = parser.parse_args()

    main(excel_filename=args.excel)
