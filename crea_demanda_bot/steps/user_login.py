# File: user_login.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def user_login(driver, matricula, password):
    time.sleep(1)
    print("Iniciando sesión...")
    driver.get("https://www.justiciacordoba.gob.ar/JusticiaCordoba/extranet.aspx")
    user_input = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.NAME, "Login$txtUserName"))
    )
    user_input.click()
    user_input.send_keys(matricula)
    user_input.send_keys(Keys.TAB)
    time.sleep(1)
    driver.switch_to.active_element.send_keys(password + Keys.ENTER)
    time.sleep(1)
    
