import os
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from config import users
from helpers.excel_updater import ExcelUpdater
from steps.user_login import user_login
import time

# Configuración básica (ajustar según tu proyecto)
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "Excel Base - Generación de Cédulas.xlsx")


# --- Setup del driver Selenium ---
from selenium.webdriver.chrome.service import Service

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    # options.add_argument('--headless')  # Descomentar si querés modo headless
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# --- Ejecución segura de steps con manejo de errores y relogin ---
def safe_step(step_func, driver, *args, **kwargs):
    """
    Ejecuta un step. Si la sesión expira o hay error, reloggea y reintenta una vez.
    """
    try:
        return step_func(driver, *args, **kwargs)
    except WebDriverException as e:
        print(f"Error en step {step_func.__name__}: {e}. Reintentando con relogin...")
        user_login(driver, users["FONSECA"])
        time.sleep(2)
        return step_func(driver, *args, **kwargs)

# --- Main loop ---
def main():
    driver = get_driver()
    try:
        # Login inicial
        print("Intentando login...")
        user_login(driver, users["FONSECA"])
        print("Login realizado.")

        # Ir al SAC para abogados y auxiliares NUEVO
        from steps.goto_sac import goto_sac
        safe_step(goto_sac, driver)
        print("Ingresado al SAC para abogados y auxiliares NUEVO.")

        time.sleep(5)

        # Inicializar helper para Excel
        excel = ExcelUpdater(EXCEL_PATH)
        print(f"Se encontraron {len(excel.df)} filas en el Excel.")

        idx = 0
        while True:
            pending_rows = excel.get_pending_rows()
            if not pending_rows:
                print("Todos los registros fueron procesados.")
                break
            row = pending_rows[0]
            # Buscar el índice real en el DataFrame por número de expediente
            row_idx = excel.df[excel.df["Número de Expte. Judicial"] == row["Número de Expte. Judicial"]].index[0]
            print(f"\n--- Procesando fila {row_idx+1} ---")
            try:
                # Buscar el expediente usando el número de la fila
                from steps.buscar_expediente import buscar_expediente
                safe_step(buscar_expediente, driver, row["Número de Expte. Judicial"])
                print(f"Buscado expediente {row['Número de Expte. Judicial']}")

                time.sleep(5)
                # Aquí seguiría la secuencia de steps: extraer info, generar PDF, etc.
                excel.mark_completed(row_idx, "completado")
            except Exception as e:
                print(f"Error procesando fila {row_idx+1}: {e}. Reintentando desde login...")
                driver.quit()
                time.sleep(2)
                driver = get_driver()
                print("Intentando login...")
                user_login(driver, users["FONSECA"])
                print("Login realizado.")
                safe_step(goto_sac, driver)
                print("Ingresado al SAC para abogados y auxiliares NUEVO.")
                excel.reload()

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
