from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
import time
import os


def _safe_click(driver, wait, by_locator, retries: int = 5):
    last_exc = None
    for _ in range(retries):
        try:
            el = wait.until(EC.element_to_be_clickable(by_locator))
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                el,
            )
            time.sleep(0.25)
            el.click()
            return
        except (ElementClickInterceptedException, StaleElementReferenceException) as e:
            last_exc = e
            try:
                el = wait.until(EC.presence_of_element_located(by_locator))
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                    el,
                )
                time.sleep(0.25)
                driver.execute_script("arguments[0].click();", el)
                return
            except Exception as js_e:
                last_exc = js_e
                time.sleep(0.5)
    if last_exc:
        raise last_exc


def case_detail(driver, case_data, numero_decreto, fecha_decreto):
    """
    Step to handle the creation of a new case (Nuevo Expediente)
    """
    wait = WebDriverWait(driver, 20)

    try:
        # Seleccionar el tipo de moneda
        print("Seleccionando tipo de moneda...")
        tipo_moneda_dropdown = wait.until(
            EC.element_to_be_clickable((By.ID, "ddlTiposMoneda"))
        )
        select_tipo_moneda = Select(tipo_moneda_dropdown)
        time.sleep(1)
        select_tipo_moneda.select_by_visible_text("$ (Pesos)")
        print("Tipo de moneda seleccionado.")
        time.sleep(1)

        # Procesar el valor del monto total para cambiar '.' por ','
        monto_total = str(case_data["Monto total"]).replace(".", ",")
        print(f"El monto total es: {monto_total}")

        # Llenar el campo de monto
        print("Ingresando monto total...")
        monto_field = wait.until(EC.presence_of_element_located((By.ID, "txtMonto")))
        monto_field.clear()
        monto_field.send_keys(monto_total)
        print("Monto total ingresado.")

        # Guardar
        print("Haciendo clic en 'Guardar'...")
        _safe_click(driver, wait, (By.ID, "btnGuardar"))
        print("'Guardar' clickeado.")

        # Desplazarse hacia abajo
        print("Haciendo scroll hasta el final de la página...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Cargar demanda
        print("Haciendo clic en 'Demanda'...")
        _safe_click(driver, wait, (By.ID, "btnDemanda"))
        print("'Demanda' clickeado.")

        time.sleep(1)

        # Seleccionar plantilla de demanda
        print("Seleccionando plantilla de demanda...")
        plantilla_demanda_dropdown = wait.until(
            EC.element_to_be_clickable((By.ID, "ddlPlantillaDemanda"))
        )
        select_plantilla_demanda = Select(plantilla_demanda_dropdown)
        time.sleep(1)
        select_plantilla_demanda.select_by_visible_text(
            "DEMANDA EJECUTIVA FISCAL MUNICIPALIDAD DE CORDOBA"
        )
        print("Plantilla de demanda seleccionada.")

        time.sleep(1)

        # Guardar demanda
        print("Haciendo scroll hasta el final de la página nuevamente...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        numero_decreto_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Numero Decreto/Año']")
            )
        )
        numero_decreto_field.clear()
        numero_decreto_field.send_keys(numero_decreto)

        fecha_decreto_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Fecha Decreto DD/MM/AA']")
            )
        )
        fecha_decreto_field.clear()
        fecha_decreto_field.send_keys(fecha_decreto)

        concepto_deuda_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Concepto Deuda']")
            )
        )
        concepto_deuda_field.clear()
        concepto_deuda_field.send_keys(case_data["Repartición"])

        numero_liquidacion_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Nro Liquidacion']")
            )
        )
        numero_liquidacion_field.clear()
        numero_liquidacion_field.send_keys(
            str(case_data["Orden"]) + "/" + str(case_data["Año"])
        )

        id_tributaria_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Id Tributaria']")
            )
        )
        id_tributaria_field.clear()
        id_tributaria_field.send_keys(case_data["Identificador"])

        time.sleep(0.5)

        print("Haciendo clic en 'Grabar'...")
        demanda_button = wait.until(EC.element_to_be_clickable((By.ID, "btnGrabar")))
        demanda_button.click()
        print("'Grabar' clickeado.")

        time.sleep(0.5)

        # Cerrar diálogo
        print("Cerrando diálogo...")
        dialog_close_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a.ui-dialog-titlebar-close.ui-corner-all")
            )
        )
        dialog_close_button.click()
        print("Diálogo cerrado.")

        time.sleep(1)

        # Volver
        print("Haciendo clic en 'Volver'...")
        volver_button = wait.until(EC.element_to_be_clickable((By.ID, "btnVolver")))
        volver_button.click()
        print("'Volver' clickeado.")

        time.sleep(1)

        # Desplazarse hacia abajo
        print("Haciendo scroll hasta el final de la página...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Adjuntos
        print("Haciendo clic en 'Adjuntos'...")
        adjuntos_button = wait.until(EC.element_to_be_clickable((By.ID, "btnAdjuntos")))
        adjuntos_button.click()
        print("'Adjuntos' clickeado.")

        time.sleep(1)

        # Desplazarse hacia abajo
        print("Haciendo scroll hasta el final de la página...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Adjuntos
        adjuntos_button = wait.until(
            EC.element_to_be_clickable((By.ID, "btnContinuar"))
        )
        adjuntos_button.click()

        ir_a_button = wait.until(EC.element_to_be_clickable((By.ID, "lnkIra")))
        ir_a_button.click()

        time.sleep(1)

    except TimeoutException:
        print("Error: No se pudo completar la creación del nuevo expediente a tiempo.")
    except NoSuchElementException as e:
        print(f"Error inesperado: {e}")
