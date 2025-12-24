from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
import time

def finish(driver):
    wait = WebDriverWait(driver, 20)

    time.sleep(1)

    ir_a_button = wait.until(EC.element_to_be_clickable((By.ID, "btnConcluir")))
    ir_a_button.click()

    time.sleep(1)

    alert = wait.until(EC.alert_is_present())
    alert = Alert(driver)
    alert.accept()

    time.sleep(5)