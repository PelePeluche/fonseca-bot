# File: upload_attachments.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def skip_attachments(driver):
    time.sleep(1)
    next_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "btnSiguiente"))
    )
    next_button.click()

    # Manejar la alerta después de hacer clic
    print("Esperando la alerta...")
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    print("Alerta presente. Aceptando la alerta...")
    alert.accept()
    print("Alerta aceptada.")
