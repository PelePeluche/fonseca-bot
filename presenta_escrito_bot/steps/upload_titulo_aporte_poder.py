import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def upload_titulo_aporte_poder(driver, title_path, planilla_path):
    time.sleep(2)

    # 1. Clic en el ícono para adjuntar poder
    try:
        print("Intentando hacer clic en el ícono para adjuntar poder...")
        poder_link = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(@onclick, 'blCargarPoder_ClienClick')]")
            )
        )
        poder_link.click()
        print("Clic en el ícono de adjuntar poder realizado.")
    except Exception as e:
        print(f"Error al hacer clic en el ícono para adjuntar poder: {e}")
        return

    # Espera para que el modal se cargue
    print("Esperando unos segundos para que el modal se cargue...")
    time.sleep(3)

    # 2. Cambiar contexto al iframe
    try:
        print("Buscando el iframe dentro del modal...")
        iframe = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "iframe.webDialogModalIFrame")
            )
        )
        print("Iframe encontrado. Cambiando el contexto al iframe...")
        driver.switch_to.frame(iframe)
    except Exception as e:
        print(f"Error al cambiar al iframe: {e}")
        return

    # 3. Seleccionar el checkbox
    try:
        print("Buscando el checkbox dentro del iframe...")
        checkbox_poder = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.ID, "grdPoderes_Row_0_column0_control_0"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_poder)
        time.sleep(1)
        print("Intentando hacer clic en el checkbox usando JavaScript directamente...")
        driver.execute_script("arguments[0].click();", checkbox_poder)
        print("Clic en el checkbox realizado.")
    except Exception as e:
        print(f"Error al buscar o hacer clic en el checkbox dentro del iframe: {e}")
        return

    # 4. Clic en botón "Adjuntar"
    try:
        print("Intentando hacer clic en el botón 'Adjuntar'...")
        adjuntar_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Adjuntar')]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", adjuntar_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", adjuntar_button)
        print("Clic en el botón 'Adjuntar' realizado.")
    except Exception as e:
        print(f"Error al hacer clic en el botón 'Adjuntar': {e}")
        return

    # 5. Manejar la alerta posterior a "Adjuntar"
    try:
        print("Esperando la alerta...")
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print("Alerta presente. Aceptando la alerta...")
        alert.accept()
        print("Alerta aceptada.")
    except Exception as e:
        print(f"Error al manejar la alerta: {e}")
        return

    # 6. Cambiar de vuelta al contexto principal
    driver.switch_to.default_content()

    # 7. Subir archivo principal (title_path) sólo si existe y no está vacío
    if title_path and title_path.strip():
        try:
            print("Buscando el input para el archivo principal...")
            file_input = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.ID, "fuAdjunto_Principal"))
            )
            file_input.send_keys(title_path)
            print("Archivo principal cargado.")
        except Exception as e:
            print(f"Error al cargar el archivo principal: {e}")
            return

        # Guardar archivo principal
        try:
            print("Buscando el botón de guardar archivo (principal)...")
            save_button = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//img[contains(@class, 'btnUploadFile') and not(@disabled)]",
                    )
                )
            )
            driver.execute_script("arguments[0].click();", save_button)
            print("Archivo principal guardado.")
        except Exception as e:
            print(f"Error al guardar el archivo principal: {e}")
            return
    else:
        print(
            "No se recibió 'title_path' válido (nulo o vacío). Omitiendo la carga del archivo principal."
        )

    # 8. Subir segundo archivo (planilla_path) sólo si existe y no está vacío
    if planilla_path and planilla_path.strip():
        try:
            print("Buscando el input para el segundo archivo...")
            file_input_second = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.ID, "fuAdjunto_Segundo"))
            )
            file_input_second.send_keys(planilla_path)
            print("Segundo archivo cargado.")
        except Exception as e:
            print(f"Error al cargar el segundo archivo: {e}")
            return

        # Guardar el segundo archivo
        try:
            print("Buscando el botón de guardar archivo para el segundo archivo...")
            save_button_second = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@id='fileContainerSegundo']//img[@class='btnUploadFile clickable' and @grupoaccion='upload']",
                    )
                )
            )

            driver.execute_script("arguments[0].click();", save_button_second)
            print("Segundo archivo guardado.")
        except Exception as e:
            print(f"Error al guardar el segundo archivo: {e}")
            return
    else:
        print(
            "No se recibió 'planilla_path' válido (nulo o vacío). Omitiendo la carga del segundo archivo."
        )

    # 9. Esperar un momento y luego clic en "Siguiente"
    time.sleep(30)
    try:
        print("Intentando hacer clic en el botón 'Siguiente'...")
        next_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.ID, "btnSiguiente"))
        )
        next_button.click()
        print("Clic en el botón 'Siguiente' realizado.")
    except Exception as e:
        print(f"Error al hacer clic en el botón 'Siguiente': {e}")
        return
