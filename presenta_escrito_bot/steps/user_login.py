from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def user_login(driver, user_config):
    driver.get("https://www.justiciacordoba.gob.ar/JusticiaCordoba/extranet.aspx")
    user_input = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.NAME, "Login$txtUserName"))
    )
    user_input.click()
    time.sleep(1)
    user_input.send_keys(user_config["matricula"])
    user_input.send_keys(Keys.TAB)
    time.sleep(1)
    driver.switch_to.active_element.send_keys(user_config["password"] + Keys.ENTER)
    time.sleep(1)
