# File: fill_presentation_data_step.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.alert import Alert
import time


def fill_presentation_data_step(driver):
    try:
        wait = WebDriverWait(driver, 30)

        time.sleep(1)

        # Wait for "Litiga en" field to be present and retry if stale element
        for _ in range(3):
            try:
                litiga_en_select = wait.until(
                    EC.presence_of_element_located((By.ID, "ddlLitigaEn"))
                )
                # Wait until the "CARGANDO" option is no longer present
                # wait.until(lambda driver: "CARGANDO" not in [option.text for option in Select(litiga_en_select).options])
                # Select an option in the "Litiga en" dropdown
                select = Select(litiga_en_select)
                select.select_by_visible_text("CORDOBA")
                break
            except StaleElementReferenceException:
                print(
                    "Stale element reference encountered for 'Litiga en'. Retrying..."
                )
                time.sleep(1)

        time.sleep(1)

        # Fill in "Group" field and retry if stale element
        for _ in range(3):
            try:
                grupo_select = wait.until(
                    EC.presence_of_element_located((By.ID, "ddlGrupo"))
                )
                # wait.until(lambda driver: "CARGANDO" not in [option.text for option in Select(grupo_select).options])
                select_grupo = Select(grupo_select)
                select_grupo.select_by_visible_text(
                    "SECRETARIA DE GESTION COMUN DE EJECUCION FISCAL"
                )
                break
            except StaleElementReferenceException:
                print("Stale element reference encountered for 'Group'. Retrying...")
                time.sleep(1)

        time.sleep(1)

        # Fill in "Category of Trial" field and retry if stale element
        for _ in range(3):
            try:
                category_trial_select = wait.until(
                    EC.presence_of_element_located(
                        (By.ID, "ddlTipoJuicio")
                    )  # Ajuste del ID según lo mostrado en la imagen
                )
                # wait.until(lambda driver: "CARGANDO" not in [option.text for option in Select(category_trial_select).options])
                select_category = Select(category_trial_select)
                select_category.select_by_visible_text(
                    "EJECUTIVO FISCAL - MUNICIPALIDAD DE CORDOBA"
                )
                break
            except StaleElementReferenceException:
                print(
                    "Stale element reference encountered for 'Category of Trial'. Retrying..."
                )
                time.sleep(1)

        # Desplazarse hacia abajo
        print("Haciendo scroll hasta el final de la página...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Click the "Save" button
        save_button = wait.until(
            EC.presence_of_element_located((By.ID, "btnContinuar"))
        )
        save_button.click()

        # Handle the alert popup
        alert = wait.until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()

    except TimeoutException as e:
        print(f"Timeout Error: {e}")
    except NoSuchElementException as e:
        print(f"Error: A form element was not found: {e}")
    except StaleElementReferenceException as e:
        print(f"Stale Element Error: {e}")
