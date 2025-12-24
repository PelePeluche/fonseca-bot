from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def goto_sac(driver, timeout=30):
    """
    Hace click en el elemento 'SAC para abogados y auxiliares NUEVO' tras el login.
    Prueba con varios selectores y toma screenshot si falla.
    """
    # Abrir la URL del SAC directamente en una nueva pestaña
    sac_url = "https://www.justiciacordoba.gob.ar/MarcoPoloNet/home"
    driver.execute_script(f"window.open('{sac_url}', '_blank');")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    return
    try:
        # 2. Intentar con XPath que busque el texto exacto en cualquier elemento
        xpath = f"//*[normalize-space(text())='{link_text}']"
        sac_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        sac_elem.click()
        return
    except Exception:
        pass
    try:
        # 3. Intentar con XPath que busque el texto parcial
        xpath_partial = f"//*[contains(normalize-space(text()), '{link_text}') or contains(., '{link_text}') ]"
        sac_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_partial))
        )
        sac_elem.click()
        return
    except Exception:
        pass
    # 4. Si todo falla, tomar screenshot para debug
    ts = int(time.time())
    driver.save_screenshot(f"sac_no_encontrado_{ts}.png")
    raise Exception(f"No se pudo encontrar el elemento SAC para abogados y auxiliares NUEVO. Se guardó screenshot como sac_no_encontrado_{ts}.png")
