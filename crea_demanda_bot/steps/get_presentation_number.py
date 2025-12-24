from selenium.webdriver.common.by import By

def get_presentation_number(driver):
    # Extraemos el número de presentación de la página
    presentation_number_element = driver.find_element(By.ID, "lblNro")
    presentation_number = presentation_number_element.text
    print(f"Número de presentación obtenido: {presentation_number}")
    return presentation_number
