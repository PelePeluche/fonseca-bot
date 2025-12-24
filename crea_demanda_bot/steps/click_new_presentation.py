# File: click_new_presentation.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def click_new_presentation(driver):
    try:
        # Esperar a que el botón de "Nueva Presentación" esté visible y hacer clic
        wait = WebDriverWait(driver, 20)
        new_presentation_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mnuNuevaPresentacion"))
        )
        new_presentation_button.click()
    except TimeoutException:
        print("Error: El botón de Nueva Presentación no se cargó a tiempo.")
    except NoSuchElementException:
        print("Error: No se encontró el botón de Nueva Presentación.")
