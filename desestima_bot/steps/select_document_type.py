# File: select_document_type.py

import time
from docx import Document
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def select_document_type(driver, document_text):
    """
    Selecciona el tipo de documento en la interfaz, convierte el texto a HTML, e inserta el texto en el campo de texto enriquecido.
    
    :param driver: Selenium WebDriver.
    :param document_text: El texto modificado que será insertado en el campo de texto enriquecido.
    """
    time.sleep(1)

    # Seleccionar el tipo de documento en el dropdown
    document_type_dropdown = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "txtIdTipoEscrito"))
    )
    document_type_dropdown.click()

    # Seleccionar la opción 'OTRAS PETICIONES'
    add_option = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'ARCHIVO - DESISTE DE LA ACCIÓN')]"))
    )
    add_option.click()

    # Convertir el texto plano en formato HTML y insertarlo
    time.sleep(1)
    html_content = text_to_html(document_text)  # Convertimos el texto en HTML
    insert_text_in_richtext(driver, html_content)

    # Hacer clic en el botón 'Siguiente'
    next_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.ID, "btnSig"))
    )
    time.sleep(1)
    next_button.click()

def text_to_html(document_text):
    """
    Convierte el texto plano en HTML. Cada línea será un párrafo <p>.
    
    :param document_text: El texto del documento en formato plano.
    :return: El contenido convertido a HTML.
    """
    lines = document_text.split('\n')
    html_content = ''.join(f"<p>{line}</p>" for line in lines if line.strip())  # Convertimos cada línea a un párrafo
    return html_content

def insert_text_in_richtext(driver, html_content):
    """
    Inserta el contenido HTML en el campo de texto enriquecido usando JavaScript.
    
    :param driver: Selenium WebDriver.
    :param html_content: El contenido en formato HTML que será insertado.
    """
    script = f"document.querySelector('.nicEdit-main').innerHTML = `{html_content}`;"
    driver.execute_script(script)
