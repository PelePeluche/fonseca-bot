# File: navigate_and_select.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def navigate_and_select(driver):
    time.sleep(2)
    written_documents_div = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "divEscritos"))
    )
    written_documents_div.click()
    new_written_link = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'Agregar Nuevo Escrito')]")
        )
    )
    new_written_link.click()
