# File: submit_case.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


def submit_case(driver):
    time.sleep(1)
    print("Submitting case...")
    submit_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "btnPresentar"))
    )

    submit_button.click()


def save_without_submission(driver):
    try:
        # Esperar y hacer clic en el botón "GUARDAR SIN PRESENTAR"
        print("Esperando el botón 'GUARDAR SIN PRESENTAR'...")
        guardar_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='GUARDAR SIN PRESENTAR']"))
        )
        guardar_button.click()
        print("Clic en el botón 'GUARDAR SIN PRESENTAR' realizado.")
        
        # Manejar la alerta después de hacer clic
        print("Esperando la alerta...")
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print("Alerta presente. Aceptando la alerta...")
        alert.accept()
        print("Alerta aceptada.")
        
    except Exception as e:
        print(f"Error al hacer clic en el botón o manejar la alerta: {e}")
        return