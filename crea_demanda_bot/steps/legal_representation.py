# File: legal_representation.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def step_legal_representation(driver, procurador, municipalidad_keyname_to_represent):
    wait = WebDriverWait(driver, 20)

    try:
        # Desplazarse hacia el botón "Nuevo Patrocinio" para asegurarse de que esté visible
        new_representation_button = driver.find_element(By.ID, "btnNuevoActorFisico")
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", new_representation_button
        )

        # Intentar hacer clic en el botón una vez que esté visible
        new_representation_button.click()
        print("Botón 'Nuevo Patrocinio' clickeado correctamente.")
    except TimeoutException:
        print("Error: El botón 'Nuevo Patrocinio' no se cargó a tiempo.")
    except Exception as e:
        print(f"Error inesperado: {e}")

    patrocinante_dropdown = wait.until(
        EC.element_to_be_clickable((By.ID, "ddlPatrocinante"))
    )
    select_patrocinante = Select(patrocinante_dropdown)
    time.sleep(1)
    select_patrocinante.select_by_visible_text(procurador)

    patrocinado_dropdown = wait.until(
        EC.element_to_be_clickable((By.ID, "ddlPatrocinado"))
    )
    select_patrocinado = Select(patrocinado_dropdown)
    time.sleep(1)
    select_patrocinado.select_by_visible_text(municipalidad_keyname_to_represent)

    time.sleep(1)

    try:
        guardar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Guardar']"))
        )
        guardar_button.click()
        print("Botón 'Guardar' clickeado correctamente.")
    except TimeoutException:
        print("Error: El botón 'Guardar' no se cargó a tiempo.")
    except Exception as e:
        print(f"Error inesperado: {e}")

    try:
        print("Intentando hacer clic en 'Ir a...'")
        ir_a_button = wait.until(EC.element_to_be_clickable((By.ID, "btnSiguiente")))
        ir_a_button.click()
        print("'Ir a...' clickeado con éxito.")

        time.sleep(2)

    except TimeoutException:
        print("Timeout: No se pudo hacer clic en 'Ir a...'.")
    except Exception as e:
        print(f"Error al hacer clic en 'Ir a...': {e}")
