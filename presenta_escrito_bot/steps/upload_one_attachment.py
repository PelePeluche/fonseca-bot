import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def upload_one_attachment(driver, attachment_path):
    # 0) Asegurémonos de que el panel de "Cargando adjuntos…" esté desaparecido
    WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.ID, "pnlCargandoAdjuntos"))
    )
    
    # 1) Esperar a que el label que acompaña al input esté visible
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
            "label[for='fuAdjunto_Principal']"))
    )
    
    # 2) Localizamos el input (ya existe en el DOM aunque esté invisible)
    file_input = driver.find_element(By.ID, "fuAdjunto_Principal")
    
    # 3) Scroll al centro de ese elemento (por si está fuera de vista)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        file_input
    )
    time.sleep(0.5)
    
    # 4) Mandamos la ruta (send_keys NO necesita que el elemento sea clickable)
    file_input.send_keys(attachment_path)
    print(f"[upload] ruta enviada: {attachment_path}")
    
    # 5) Localizamos el botón de “Grabar Adjunto” dentro de su contenedor
    save_btn = driver.find_element(
        By.XPATH,
        "//div[@id='fileContainerPrincipal']//img[contains(@class,'btnUploadFile')]"
    )
    
    # 6) Click vía JS (para evitar solapamientos)
    driver.execute_script("arguments[0].click();", save_btn)
    print("[upload] clic en Grabar Adjunto")
    
    # 7) Esperar a que el ícono desaparezca (subida completada)
    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located((
            By.XPATH,
            "//div[@id='fileContainerPrincipal']//img[contains(@class,'btnUploadFile')]"
        ))
    )
    print("[upload] adjunto cargado ✔️")
    
    # 8) Pequeña pausa antes de seguir
    time.sleep(15)


# 9) Localizar y clickear el botón “Siguiente”
    print("[upload] Esperando botón SIGUIENTE...")
    next_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnSiguiente"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
    time.sleep(0.3)
    print("[upload] Haciendo click en SIGUIENTE")
    next_btn.click()
    print("[upload] Click en SIGUIENTE realizado ✔️")

    # 10) Pequeña pausa final si necesitás
    time.sleep(1)