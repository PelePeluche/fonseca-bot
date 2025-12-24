from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


def step_new_case(driver):
    """
    Step to handle the creation of a new case (Nuevo Expediente)
    """
    wait = WebDriverWait(driver, 20)

    try:
        # Click on "Nuevo Expediente" button
        new_case_button = wait.until(
            EC.element_to_be_clickable((By.ID, "lnkNuevoExpediente"))
        )
        new_case_button.click()
        print("Botón 'Nuevo Expediente' clickeado correctamente.")

    except TimeoutException:
        print("Error: No se pudo completar la creación del nuevo expediente a tiempo.")
    except NoSuchElementException as e:
        print(f"Error inesperado: {e}")
