import os
import pandas as pd
from steps.driver_setup import setup_driver
from steps.user_login import user_login
from steps.manage_tabs import open_new_tab
from steps.click_new_presentation import click_new_presentation
from steps.fill_presentation_data_step import fill_presentation_data_step
from steps.step2_common_parts import step_2_common_parts
from steps.legal_representation import step_legal_representation
from steps.new_case_step import step_new_case
from steps.case_detail_without_attachment import case_detail
from steps.get_presentation_number import get_presentation_number
from steps.finish import finish
from config import users


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_path, "tables", "NOT FOUND PARA INICIAR TF RAMIRO SONZINI.xlsx")

    # Verificamos si el archivo Excel existe
    if not os.path.exists(excel_path):
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


def execute_steps(driver, row):
    # Creamos el objeto case_data con los datos relevantes de la fila
    case_data = {
        "Archivo": row["Archivo"],
        "Nombre o Razón Social": row["Nombre o Razón Social"],
        "CUIT": str(row["CUIT"]).split(".")[0] if row["CUIT"] else None,
        "Repartición": row["Repartición"],
        "Orden": str(row["Orden"]).split(".")[0] if row["Orden"] else None,
        "Año": str(row["Año"]).split(".")[0] if row["Año"] else None,
        "Identificador": (
            str(row["Identificador"]).split(".")[0] if row["Identificador"] else None
        ),
        "Domicilio": row["Domicilio"],
        "Monto total": row["Monto total"],
        "Tipo de Persona": row["Tipo de Persona"],
    }

    user_key = "SONZINI"

    username = users[user_key]["matricula"]
    password = users[user_key]["password"]
    procurador = users[user_key]["procurador"]
    numero_decreto = users[user_key]["numero_decreto"]
    fecha_decreto = users[user_key]["fecha_decreto"]
    municipalidad_keyname_to_search = users[user_key]["municipalidad_keyname_to_search"]
    municipalidad_keyname_to_represent = users[user_key]["municipalidad_keyname_to_represent"]

    # Ejecutamos los steps necesarios con el driver
    user_login(driver, username, password)
    open_new_tab(driver)
    click_new_presentation(driver)
    fill_presentation_data_step(driver)
    step_2_common_parts(driver, case_data, municipalidad_keyname_to_search)
    step_legal_representation(driver, procurador, municipalidad_keyname_to_represent)
    step_new_case(driver)
    case_detail(driver, case_data, numero_decreto, fecha_decreto)
    presentation_number = get_presentation_number(driver)
    finish(driver)

    return presentation_number


if __name__ == "__main__":
    main()