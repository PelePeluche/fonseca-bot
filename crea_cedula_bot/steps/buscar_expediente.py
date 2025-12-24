from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def buscar_expediente(driver, numero_expediente, timeout=20):
    """
    Busca un expediente en el buscador superior usando el número de expediente judicial.
    """
    # Intentar primero el input del header
    try:
        input_elem = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Buscar por N° Expediente...']"))
        )
        print("Usando input del header para búsqueda rápida.")
    except Exception:
        # Si no está, intentar el input de búsqueda avanzada
        try:
            input_elem = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='nroExpediente']"))
            )
            print("Usando input del formulario de búsqueda avanzada.")
        except Exception:
            raise Exception("No se encontró el input de búsqueda de expediente ni en el header ni en el formulario avanzado.")

    input_elem.clear()
    input_elem.send_keys(str(numero_expediente))
    input_elem.send_keys(Keys.ENTER)
