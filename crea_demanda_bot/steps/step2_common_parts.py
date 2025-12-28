from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    NoSuchElementException,
)
import time

# File: step2_common_parts.py


def _safe_click(driver, wait, by_locator, retries: int = 5):
    last_exc: Exception | None = None
    for _ in range(retries):
        try:
            el = wait.until(EC.element_to_be_clickable(by_locator))
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                el,
            )
            time.sleep(0.25)
            el.click()
            return
        except (ElementClickInterceptedException, StaleElementReferenceException) as e:
            last_exc = e
            try:
                el = wait.until(EC.presence_of_element_located(by_locator))
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                    el,
                )
                time.sleep(0.25)
                driver.execute_script("arguments[0].click();", el)
                return
            except Exception as js_e:
                last_exc = js_e
                time.sleep(0.5)
    if last_exc:
        raise last_exc


def step_2_common_parts(driver, case_data, municipalidad_keyname_to_search):
    """
    Completes Step 2: COMMON PARTS TO THE ENTIRE PRESENTATION.
    Includes editing the already loaded lawyer information, adding the 'Municipalidad de Córdoba',
    and adding a new person (física or jurídica) based on the case_data.
    """
    try:
        wait = WebDriverWait(driver, 20)

        # Wait and click on the edit button for the already loaded lawyer
        edit_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "img#grdActores_Row_0_column8_control_0.ImageButton.btnEditar",
                )
            )
        )
        edit_button.click()

        time.sleep(1)

        # Fill in the address if it is empty
        for attempt in range(7):
            try:
                address_field = wait.until(
                    EC.presence_of_element_located((By.ID, "txtDireccion"))
                )
                current_value = address_field.get_attribute("value")
                print(f"DEBUG: Valor actual de 'txtDireccion': '{current_value}'")
                
                if not current_value or current_value.strip() == "" or "sin datos" in current_value.lower():
                    print("Detectado campo vacío o 'Sin Datos'. Rellenando dirección...")
                    address_field.click()
                    address_field.clear()
                    address_field.send_keys("MARCELO T. DE ALVEAR 120, TERCER PISO")
                    break
                else:
                    print("El campo dirección ya tiene datos válidos.")
                    break
            except (StaleElementReferenceException, NoSuchElementException):
                time.sleep(1)

        # Click on the save button
        _safe_click(driver, wait, (By.ID, "btnGuardar"))

        # Add the "Municipalidad de Córdoba"
        new_legal_party_button = wait.until(
            EC.element_to_be_clickable((By.ID, "btnNuevoActorJuridico"))
        )
        new_legal_party_button.click()

        contact_search_icon = wait.until(
            EC.element_to_be_clickable((By.ID, "btnAbrirAgenda"))
        )
        contact_search_icon.click()

        search_input = wait.until(
            EC.presence_of_element_located((By.ID, "txtFiltroRazonSocial"))
        )
        search_input.clear()
        search_input.send_keys(municipalidad_keyname_to_search)

        search_button = wait.until(EC.element_to_be_clickable((By.ID, "btnBuscar")))
        search_button.click()

        time.sleep(1)

        search_result = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "td#grdAgendaJuridica_Row_0_column0 div.divCellData")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView();", search_result)
        driver.execute_script("arguments[0].click();", search_result)

        # Fill in the "Rol" field
        rol_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "ddlIdTipoRol")))
        rol_dropdown.click()

        select = Select(rol_dropdown)
        select.select_by_visible_text("ACTOR PRINCIPAL")

        # Click on the "Guardar" button after adding "Municipalidad de Córdoba"
        _safe_click(driver, wait, (By.ID, "btnGuardar"))

        time.sleep(1)

        # Now, based on the "Tipo de Persona", add a new person (física or jurídica)
        tipo_persona = case_data.get("Tipo de Persona", "").lower().strip()
        print(f"DEBUG: Tipo de Persona leído del Excel: '{tipo_persona}'")

        if tipo_persona in ["física", "fisica"]:
            # Add a new physical person
            new_human_button = wait.until(
                EC.element_to_be_clickable((By.ID, "btnNuevoActorFisico"))
            )
            new_human_button.click()
            
            print("Botón 'Nuevo Actor Físico' clickeado.")
            time.sleep(1)

            fill_human_part_form(driver, case_data)

        elif tipo_persona in ["jurídica", "juridica"]:
            # Add a new legal entity
            new_legal_entity_button = wait.until(
                EC.element_to_be_clickable((By.ID, "btnNuevoActorJuridico"))
            )
            new_legal_entity_button.click()

            time.sleep(1)

            fill_juridical_part_form(driver, case_data)

        else:
            print(
                f"Tipo de Persona '{tipo_persona}' no reconocido. No se agregará ninguna parte."
            )

        time.sleep(1)

        # Desplazarse hacia abajo
        print("Haciendo scroll hasta el final de la página...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Final click on "Ir a..."
        try:
            print("Intentando hacer clic en 'Ir a...'")
            ir_a_button = wait.until(
                EC.element_to_be_clickable((By.ID, "btnSiguiente"))
            )
            ir_a_button.click()
            print("'Ir a...' clickeado con éxito.")

        except TimeoutException:
            print("Timeout: No se pudo hacer clic en 'Ir a...'.")
        except Exception as e:
            print(f"Error al hacer clic en 'Ir a...': {e}")

    except TimeoutException:
        print("Timeout: Could not complete step 2.")
        raise
    except Exception as e:
        print(f"Error completing step 2: {e}")
        raise


def fill_juridical_part_form(driver, case_data):
    """
    Fills out the 'Parte Jurídica' form based on the provided case_data.
    """
    wait = WebDriverWait(driver, 20)

    # 1. Select 'Rol'
    try:
        rol_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "ddlIdTipoRol")))
        select_rol = Select(rol_dropdown)
        # Cambia esto si el rol es diferente
        select_rol.select_by_visible_text("DEMANDADO PRINCIPAL")
        print("Rol seleccionado.")
    except TimeoutException:
        print("Timeout: No se pudo seleccionar el rol.")

    # 2. Fill 'Razón Social'
    try:
        razon_social_field = wait.until(
            EC.presence_of_element_located((By.ID, "txtRazonSocial"))
        )
        razon_social_field.clear()
        razon_social_field.send_keys(case_data["Nombre o Razón Social"])
        print("Razón Social ingresada.")
    except TimeoutException:
        print("Timeout: No se pudo ingresar la razón social.")

    # 3. Fill 'CUIT'
    try:
        cuit_field = wait.until(
            EC.presence_of_element_located((By.ID, "txtNumeroDocumento"))
        )
        cuit_field.clear()
        cuit_field.send_keys(case_data["CUIT"])
        print("CUIT ingresado.")
    except TimeoutException:
        print("Timeout: No se pudo ingresar el CUIT.")

    # 4. Select 'Tipo de Domicilio'
    try:
        tipo_domicilio_dropdown = wait.until(
            EC.element_to_be_clickable((By.ID, "ddlIdTipoDomicilio"))
        )
        select_tipo_domicilio = Select(tipo_domicilio_dropdown)
        select_tipo_domicilio.select_by_visible_text("DOMICILIO FISCAL")
        print("Tipo de Domicilio seleccionado.")
    except TimeoutException:
        print("Timeout: No se pudo seleccionar el tipo de domicilio.")

    # 5. Fill 'Dirección'
    try:
        direccion_field = wait.until(
            EC.presence_of_element_located((By.ID, "txtDireccion"))
        )
        direccion_field.clear()
        direccion_field.send_keys(case_data["Domicilio"])
        print("Dirección ingresada.")
    except TimeoutException:
        print("Timeout: No se pudo ingresar la dirección.")

    # 6. Fill 'Localidad'
    try:
        localidad_field = wait.until(
            EC.presence_of_element_located((By.ID, "txtLocalidad"))
        )
        localidad_field.clear()
        localidad_field.send_keys("Córdoba")
        print("Localidad ingresada.")
    except TimeoutException:
        print("Timeout: No se pudo ingresar la localidad.")

    tipo_domicilio_dropdown = wait.until(
        EC.element_to_be_clickable((By.ID, "ddlIdTipoDomicilio"))
    )
    select_tipo_domicilio = Select(tipo_domicilio_dropdown)
    select_tipo_domicilio.select_by_visible_text("DOMICILIO REAL")

    time.sleep(2)

    # Desplazarse hacia abajo
    print("Haciendo scroll hasta el final de la página...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 8. Click 'Guardar'
    try:
        _safe_click(driver, wait, (By.ID, "btnGuardar"))
        print("Formulario guardado.")
    except TimeoutException:
        print("Timeout: No se pudo hacer click en 'Guardar'.")


def fill_human_part_form(driver, case_data):
    """
    Fills out the 'Parte Humana' form based on the provided case_data.
    """
    wait = WebDriverWait(driver, 20)

    [apellido, nombre] = split_name_simple(case_data["Nombre o Razón Social"])

    time.sleep(1)

    # Select 'Rol'
    rol_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "ddlIdTipoRol")))
    select_rol = Select(rol_dropdown)
    select_rol.select_by_visible_text(
        "DEMANDADO PRINCIPAL"
    )  # Usamos 'ACTOR PRINCIPAL' como valor por defecto.

    # Fill 'Nombre'
    nombre_field = wait.until(EC.presence_of_element_located((By.ID, "txtNombre")))
    nombre_field.clear()
    nombre_field.send_keys(nombre)

    # Fill 'Apellido'
    apellido_field = wait.until(EC.presence_of_element_located((By.ID, "txtApellido")))
    apellido_field.clear()
    apellido_field.send_keys(apellido)

    # Select 'Sexo'
    sexo_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "ddlIdTipoSexo")))
    select_sexo = Select(sexo_dropdown)
    select_sexo.select_by_visible_text("Desconocido")

    # Select 'Tipo de Documento'
    tipo_documento_dropdown = wait.until(
        EC.element_to_be_clickable((By.ID, "ddlIdTipoDocumento"))
    )
    select_tipo_documento = Select(tipo_documento_dropdown)
    select_tipo_documento.select_by_visible_text("MI")

    # Fill 'Número de Documento'
    numero_documento_field = wait.until(
        EC.presence_of_element_located((By.ID, "txtNumeroDocumento"))
    )
    numero_documento_field.clear()
    cuit_value = (
        "00000000000" if case_data["CUIT"] == "No especificado" else case_data["CUIT"]
    )
    numero_documento_field.send_keys(cuit_value)

    # Fill 'Dirección'
    direccion_field = wait.until(
        EC.presence_of_element_located((By.ID, "txtDireccion"))
    )
    direccion_field.clear()
    direccion_field.send_keys(case_data["Domicilio"])

    tipo_domicilio_dropdown = wait.until(
        EC.element_to_be_clickable((By.ID, "ddlIdTipoDomicilio"))
    )
    select_tipo_domicilio = Select(tipo_domicilio_dropdown)
    select_tipo_domicilio.select_by_visible_text("DOMICILIO REAL")

    # Fill 'Localidad'
    localidad_field = wait.until(
        EC.presence_of_element_located((By.ID, "txtLocalidad"))
    )
    localidad_field.clear()
    localidad_field.send_keys("Córdoba")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    # Click the 'Guardar' button
    _safe_click(driver, wait, (By.ID, "btnGuardar"))


def split_name_simple(full_name):
    # Dividimos el nombre completo en partes
    parts = full_name.split()

    # El primer elemento es el apellido
    apellido = parts[0]

    # El resto es el nombre
    nombre = " ".join(parts[1:])

    return apellido, nombre
