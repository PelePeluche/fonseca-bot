from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os


def case_detail_escaneados(driver, case_data, numero_decreto, fecha_decreto):
    """
    Step to handle the creation of a new case (Nuevo Expediente)
    """
    wait = WebDriverWait(driver, 20)

    otros_si_digo = "Que manifiesto bajo fe de juramento que mi nombramiento como Procurador Municipal efectuado por Resolución N° 187/2020 del 20/04/2020 de la Secretaría de Economía y Finanzas de la Municipalidad de Córdoba se encuentra vigente, subsistiendo al día de la fecha, ratificando en todos sus términos la juramentación realizada oportunamente."

    try:
        # Obtener el directorio base del archivo actual
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Definir la ruta hacia la carpeta en un nivel superior
        title_path = os.path.join(
            base_path, os.pardir, os.pardir, "titles", "INICIAR TRIBUNAL DE FALTAS DICIEMBRE 2025 SONZINI (22-12-2025)", case_data["Archivo"]
        )

        # Convertir la ruta a su forma absoluta
        title_path = os.path.abspath(title_path)
        print(f"Ruta del archivo a cargar: {title_path}")

        # Seleccionar el tipo de moneda
        print("Seleccionando tipo de moneda...")
        tipo_moneda_dropdown = wait.until(
            EC.element_to_be_clickable((By.ID, "ddlTiposMoneda"))
        )
        select_tipo_moneda = Select(tipo_moneda_dropdown)
        time.sleep(1)
        select_tipo_moneda.select_by_visible_text("$ (Pesos)")
        print("Tipo de moneda seleccionado.")
        time.sleep(1)

        # Procesar el valor del monto total para cambiar '.' por ','
        monto_total = str(case_data["Monto total"]).replace(".", ",")
        print(f"El monto total es: {monto_total}")

        # Llenar el campo de monto
        print("Ingresando monto total...")
        monto_field = wait.until(EC.presence_of_element_located((By.ID, "txtMonto")))
        monto_field.clear()
        monto_field.send_keys(monto_total)
        print("Monto total ingresado.")

        # Guardar
        print("Haciendo clic en 'Guardar'...")
        guardar_button = wait.until(EC.element_to_be_clickable((By.ID, "btnGuardar")))
        guardar_button.click()
        print("'Guardar' clickeado.")

        # Desplazarse hacia abajo
        print("Haciendo scroll hasta el final de la página...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Cargar demanda
        print("Haciendo clic en 'Demanda'...")
        demanda_button = wait.until(EC.element_to_be_clickable((By.ID, "btnDemanda")))
        demanda_button.click()
        print("'Demanda' clickeado.")

        time.sleep(1)

        # Seleccionar plantilla de demanda
        print("Seleccionando plantilla de demanda...")
        plantilla_demanda_dropdown = wait.until(
            EC.element_to_be_clickable((By.ID, "ddlPlantillaDemanda"))
        )
        select_plantilla_demanda = Select(plantilla_demanda_dropdown)
        time.sleep(1)
        select_plantilla_demanda.select_by_visible_text(
            "DEMANDA EJECUTIVA FISCAL"
        )
        print("Plantilla de demanda seleccionada.")

        time.sleep(1)

        # Guardar demanda
        print("Haciendo scroll hasta el final de la página nuevamente...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        concepto_deuda_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Concepto Deuda']")
            )
        )
        concepto_deuda_field.clear()
        concepto_deuda_field.send_keys(case_data["Repartición"])

        numero_liquidacion_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Nro Liquidacion']")
            )
        )
        numero_liquidacion_field.clear()
        numero_liquidacion_field.send_keys(
            str(case_data["Orden"]) + "/" + str(case_data["Año"])
        )

        case_nro_field = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='Id Tributaria']")
    )
)
        case_nro_field.clear()

        # Convierte el valor a entero y luego a cadena
        case_number = str(int(case_data["Causa Nro."]))
        case_nro_field.send_keys(case_number)


        print("Buscando el editor visual 'OTROSI DIGO'...")
        # Localizar el div editable
        editor = driver.find_element(By.CSS_SELECTOR, "div.nicEdit-main[contenteditable='true']")
        
        time.sleep(1)

        print("Escribiendo en el editor visual...")
        editor.clear()  # Limpiar cualquier texto previo
        editor.send_keys(otros_si_digo)
        print("Texto escrito exitosamente en 'OTROSI DIGO'.")

        time.sleep(0.5)

        print("Haciendo clic en 'Grabar'...")
        demanda_button = wait.until(EC.element_to_be_clickable((By.ID, "btnGrabar")))
        demanda_button.click()
        print("'Grabar' clickeado.")

        time.sleep(0.5)

        # Cerrar diálogo
        print("Cerrando diálogo...")
        dialog_close_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a.ui-dialog-titlebar-close.ui-corner-all")
            )
        )
        dialog_close_button.click()
        print("Diálogo cerrado.")

        time.sleep(0.5)

        # Volver
        print("Haciendo clic en 'Volver'...")
        volver_button = wait.until(EC.element_to_be_clickable((By.ID, "btnVolver")))
        volver_button.click()
        print("'Volver' clickeado.")

        time.sleep(0.5)

              # Desplazarse hacia abajo
        print("Haciendo scroll hasta el final de la página...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        # Adjuntos
        print("Haciendo clic en 'Adjuntos'...")
        adjuntos_button = wait.until(EC.element_to_be_clickable((By.ID, "btnAdjuntos")))
        adjuntos_button.click()
        print("'Adjuntos' clickeado.")

        time.sleep(1)

        # Seleccionar tipo de archivo
        print("Seleccionando tipo de archivo...")
        tipo_archivo_dropdown = wait.until(
            EC.element_to_be_clickable((By.ID, "ddlTiposAdjuntoExpediente"))
        )
        select_tipo_archivo = Select(tipo_archivo_dropdown)
        time.sleep(1)
        select_tipo_archivo.select_by_visible_text("Título Ejecutivo - Otros")
        print("Tipo de archivo seleccionado.")

        time.sleep(1)

        # Cargar archivo
        print("Verificando si el campo de archivo está presente y es interactuable...")
        file_input = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.ID, "fuArchivo"))
        )

        file_input.send_keys(title_path)

        agregar_button = wait.until(
            EC.element_to_be_clickable((By.ID, "btnAgregarArchivo"))
        )
        agregar_button.click()

        time.sleep(2)

        dialog_close_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.ui-icon-closethick"))
        )
        dialog_close_button.click()

        # Desplazarse hacia abajo
        print("Haciendo scroll hasta el final de la página...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Adjuntos
        adjuntos_button = wait.until(
            EC.element_to_be_clickable((By.ID, "btnContinuar"))
        )
        adjuntos_button.click()

        ir_a_button = wait.until(EC.element_to_be_clickable((By.ID, "lnkIra")))
        ir_a_button.click()

        time.sleep(1)

    except TimeoutException:
        print("Error: No se pudo completar la creación del nuevo expediente a tiempo.")
    except NoSuchElementException as e:
        print(f"Error inesperado: {e}")
