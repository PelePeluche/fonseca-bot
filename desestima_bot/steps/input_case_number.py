# File: input_case_number.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def input_case_number(driver, case_number):
    """
    Ingresa el número de expediente en el formulario.

    :param driver: WebDriver de Selenium.
    :param case_number: Número del caso (se asegura que sea un entero).
    """
    try:
        # Asegurarnos de que sea un entero
        case_number = int(case_number)
    except ValueError:
        raise ValueError(f"El número del caso '{case_number}' no es válido. Debe ser un número entero.")

    time.sleep(1)
    case_input = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "txtIdExpediente"))
    )
    case_input.click()
    case_input.send_keys(case_number)
    
    search_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.input-group-text"))
    )
    search_button.click()
    time.sleep(1)
    
    add_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "btnAddExpedientesPorNumero"))
    )
    add_button.click()
    time.sleep(1)
    
    next_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "btnSig"))
    )
    next_button.click()
    
    # Manejo de alertas
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
