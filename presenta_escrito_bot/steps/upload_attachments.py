# File: upload_attachments.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def upload_attachments(driver, file_path):
    time.sleep(1)
    file_input = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, "fuAdjunto_Principal"))
    )
    file_input.send_keys(file_path)
    file_input.get_attribute("value")
    save_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btnUploadFile"))
    )
    save_button.click()
    time.sleep(15)
    next_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "btnSiguiente"))
    )
    next_button.click()
