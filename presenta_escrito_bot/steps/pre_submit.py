# File: pre_submit.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def pre_submit(driver):
    time.sleep(1)
    submit_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "btnPresentarFinal"))
    )
    submit_button.click()
    time.sleep(1)
