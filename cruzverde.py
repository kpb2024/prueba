from scrapy.selector import Selector
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import logging
import shutil
import re
import os
import pandas as pd
from datetime import date, datetime
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys 

import traceback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def tiempo_transcurrido(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{horas:02.0f}:{minutos:02.0f}:{segundos:02.0f}"

def hacer_login(driver):
    try:
        # Navegar a la página principal
        driver.get('https://femsab2b.bbr.cl/SaludCL/BBRe-commerce/main')
        time.sleep(1)

        # Esperar a que el input esté presente y visible en la página
        input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/div[2]/div/div/div[2]/div/div/form/div[1]/input"))
        )
        input_element.click()
        time.sleep(1)
        input_element.send_keys("marcelo.flores@grchile.cl")
        # logging.info("Correo ingresado correctamente.")
        time.sleep(1)

        # Seleccionar el campo de contraseña
        input_password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/div[2]/div/div/div[2]/div/div/form/div[2]/input"))
        )
        time.sleep(1)
        input_password.click()
        input_password.send_keys("bemfola2025")
        # logging.info("Contraseña ingresada correctamente.")

        # Hacer clic en el botón de inicio de sesión
        input_botonInicioSesion = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/div[2]/div/div/div[2]/div/div/form/div[4]/input[2]"))
        )
        time.sleep(1)
        input_botonInicioSesion.click()
        time.sleep(2)

        logging.info("✅ Login realizado correctamente.")
        return True

    except Exception as e:
        logging.error(f"❌ Error durante el login: {e}")
        return False

def realizar_navegacion(driver):
    try:
        # Hacer clic en el botón del menú
        boton_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/vaadin-vertical-layout/app-box/app-header/app-toolbar/paper-icon-button[1]"))
        )
        time.sleep(1)
        boton_menu.click()
        # logging.info("Botón de menú clickeado correctamente.")
        time.sleep(1)

        # Hacer clic en el botón de "comercial y abastecimiento"
        boton_comerci_abast = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/vaadin-vertical-layout/app-box/app-drawer[1]/div/vaadin-vertical-layout/div[2]/div[4]/div"))
        )
        time.sleep(1)
        boton_comerci_abast.click()
        # logging.info("Botón de menú comercial y abastecimiento clickeado correctamente.")
        time.sleep(1)

        #  Hacer clic en el botón de "periodo"
        boton_periodo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/vaadin-vertical-layout/app-box/app-drawer[1]/div/vaadin-vertical-layout/div[2]/div[1]/div"))
        )
        time.sleep(1)
        boton_periodo.click()
        logging.info("Botón de menú periodo clickeado correctamente.")
        time.sleep(3)

        return True  # Indica que la navegación fue exitosa

    except Exception as e:
        logging.error(f"❌ Error durante la navegación: {e}")
        return False  # Indica que hubo un error

def entrar_iframe(driver):
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bbr-iframe"))
    )
    driver.switch_to.frame(iframe)
    # logging.info("Cambiado al contexto del iframe correctamente.")

def salir_iframe(driver):
    driver.switch_to.default_content()
    logging.info("✅ Se salio del iframe ")

def modificar_filtro_fecha_dentro_iframe(driver):
    try:

        time.sleep(2)  # Esperar a que cargue el contenido dentro del iframe
        fecha_ayer = (datetime.today() - timedelta(days=1)).strftime("%d-%m-%Y")
        time.sleep(1)
        # Esperar el vaadin-date-picker y acceder a su Shadow DOM
        date_picker = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-date-picker.bbr-filter-fields"))
        )
        time.sleep(1)
        shadow_root_1 = driver.execute_script("return arguments[0].shadowRoot", date_picker)

        # Ubicar vaadin-date-picker-text-field dentro del Shadow DOM
        date_picker_text_field = WebDriverWait(shadow_root_1, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-date-picker-text-field"))
        )

        shadow_root_2 = driver.execute_script("return arguments[0].shadowRoot", date_picker_text_field)

        # Ubicar el input dentro del segundo Shadow DOM
        input_field = WebDriverWait(shadow_root_2, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[part='value']"))
        )

        # Modificar el valor del input
        input_field.click()
        time.sleep(1)
        input_field.clear()
        time.sleep(1)
        input_field.send_keys(fecha_ayer)
        logging.info(f"Fecha {fecha_ayer} ingresada correctamente en el filtro.")
        input_field.send_keys(Keys.RETURN)  # Presionar Enter para confirmar la fecha   

        time.sleep(2)

    except Exception as e:
        logging.error(f"Error al modificar el filtro de fecha dentro del iframe: {e}")
        driver.switch_to.default_content()

def interactuar_con_boton_dentro_iframe(driver):
    try:
        time.sleep(3)

        # Esperar a que el vaadin-button esté presente
        boton_vaadin = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#action_drawer vaadin-button"))
        )

        # Acceder al shadow root del vaadin-button
        shadow_root = driver.execute_script("return arguments[0].shadowRoot", boton_vaadin)

        # Dentro del shadowRoot, buscar el botón real
        boton_real = shadow_root.find_element(By.CSS_SELECTOR, "button")

        # Hacer clic en el botón real
        boton_real.click()
        logging.info("Botón clickeado correctamente dentro del iframe.")
        time.sleep(5)

    except Exception as e:
        logging.error(f"Error al interactuar con el botón dentro del iframe: {e}")
        driver.switch_to.default_content()

def descargar_archivo(driver):
    try:
        time.sleep(1)
        # logging.info("🔍 Buscando botón de descarga...")

            # Esperar a que 'vaadin-vertical-layout' esté presente
        vaadin_vertical_layout = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-vertical-layout.no-margin.bbr-app"))
        )
        # logging.info("✅ vaadin-vertical-layout encontrado.")

        # Obtener el shadow root de vaadin-vertical-layout
        shadow_root_vertical = driver.execute_script("return arguments[0].shadowRoot", vaadin_vertical_layout)
        # logging.info("✅ shadow_root_vertical encontrado.")

        slot_element = shadow_root_vertical.find_element(By.CSS_SELECTOR, "slot")
        # logging.info("✅ Slot encontrado.")

        vaadin_horizontal_layout = driver.execute_script(
            "return arguments[0].assignedElements()[1];",
            slot_element
        )
        # logging.info("✅ vaadin-horizontal-layout encontrado.")

        # Obtener el shadow root de vaadin-horizontal-layout
        shadow_root_horizontal = driver.execute_script("return arguments[0].shadowRoot", vaadin_horizontal_layout)
        # logging.info("✅ shadow_root_horizontal encontrado.")

        slot_horizontal = shadow_root_horizontal.find_element(By.CSS_SELECTOR, "slot")
        # logging.info("✅ Slot en vaadin-horizontal-layout encontrado.")

        # Acceder al elemento 'vertical-toolbar' dentro del slot
        vertical_toolbar = driver.execute_script(
            "return arguments[0].assignedElements()[1];", slot_horizontal  # Cambiar índice si es necesario
        )
        # logging.info("✅ vertical-toolbar encontrado.")

        # Buscar el contenedor de botones dentro del shadow root
        t_vertical_toolbar = vertical_toolbar.find_element(By.CSS_SELECTOR, ".t-vertical-toolbar")
        # logging.info("✅ t-vertical-toolbar encontrado.")

        # Buscar el botón de descarga
        boton_descarga = t_vertical_toolbar.find_element(By.CSS_SELECTOR, "paper-icon-button.btn-download")

        # Hacer scroll hasta el botón y hacer clic
        driver.execute_script("arguments[0].scrollIntoView();", boton_descarga)
        time.sleep(1)  # Pequeña espera para evitar problemas de renderizado
        boton_descarga.click()
        logging.info("✅ Se hizo clic en el botón de descarga.")

    except Exception as e:
        logging.error(f"Error al interactuar con el botón dentro del iframe: {e}")
        driver.switch_to.default_content() 

def obtener_nombre_producto(driver):
        try:
            # logging.info("🔍 Buscando título del producto...")

            # 1️⃣ Esperar a que 'vaadin-vertical-layout' esté presente
            vaadin_vertical_layout = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-vertical-layout.no-margin.bbr-app"))
            )
            # logging.info("✅ vaadin-vertical-layout encontrado.")

            # 2️⃣ Obtener el shadow root de vaadin-vertical-layout
            shadow_root_vertical = driver.execute_script("return arguments[0].shadowRoot", vaadin_vertical_layout)
            # logging.info("✅ shadow_root_vertical encontrado.")

            # 3️⃣ Buscar el vaadin-horizontal-layout con clase "bbr-report-view-header"
            vaadin_header_layout = WebDriverWait(shadow_root_vertical, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-horizontal-layout.bbr-report-view-header"))
            )
            # logging.info("✅ vaadin-horizontal-layout con clase 'bbr-report-view-header' encontrado.")

            # 4️⃣ Acceder al shadow-root de vaadin-horizontal-layout
            shadow_root_header = driver.execute_script("return arguments[0].shadowRoot", vaadin_header_layout)
            # logging.info("✅ shadow_root_header encontrado.")

            # 5️⃣ Buscar el slot dentro del shadow-root
            slot_element = WebDriverWait(shadow_root_header, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "slot"))
            )
            # logging.info("✅ Slot encontrado en shadow_root_header.")

            # 6️⃣ Obtener los elementos asignados en el slot (deberían incluir los labels)
            assigned_labels = driver.execute_script("return arguments[0].assignedElements();", slot_element)
            if not assigned_labels:
                # logging.error("❌ No se encontraron labels dentro del slot.")
                return None

            # 7️⃣ DEBUG: Mostrar los elementos encontrados en el slot
            for i, elem in enumerate(assigned_labels):
                logging.info(f"🔍 Elemento {i}: Tag={elem.tag_name}, Clases={elem.get_attribute('class')}, Texto={elem.text.strip()}")

            # 8️⃣ Buscar el label con clase "bbr-report-view-header-title"
            label_titulo = next(
                (label for label in assigned_labels if "bbr-report-view-header-title" in label.get_attribute("class")),
                None
            )

            if not label_titulo:
                # logging.error("❌ No se encontró el label con clase 'bbr-report-view-header-title'.")
                return None

            # ✅ Obtener el texto del label
            texto_label = label_titulo.text.strip()
            # logging.info(f"✅ Nombre del producto: {texto_label}")

            return texto_label

        except Exception as e:
            logging.error(f"❌ Error al obtener el nombre del producto: {e}")
            return None

def clickear_en_volver(driver):
    try:
        time.sleep(2)
        # logging.info("🔍 Buscando botón de descarga...")

            # Esperar a que 'vaadin-vertical-layout' esté presente
        vaadin_vertical_layout = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-vertical-layout.no-margin.bbr-app"))
        )
        # logging.info("✅ vaadin-vertical-layout encontrado.")

        # Obtener el shadow root de vaadin-vertical-layout
        shadow_root_vertical = driver.execute_script("return arguments[0].shadowRoot", vaadin_vertical_layout)
        # logging.info("✅ shadow_root_vertical encontrado.")

        slot_element = shadow_root_vertical.find_element(By.CSS_SELECTOR, "slot")
        # logging.info("✅ Slot encontrado.")

        vaadin_horizontal_layout = driver.execute_script(
            "return arguments[0].assignedElements()[1];",
            slot_element
        )
        # logging.info("✅ vaadin-horizontal-layout encontrado.")

        # Obtener el shadow root de vaadin-horizontal-layout
        shadow_root_horizontal = driver.execute_script("return arguments[0].shadowRoot", vaadin_horizontal_layout)
        # logging.info("✅ shadow_root_horizontal encontrado.")

        slot_horizontal = shadow_root_horizontal.find_element(By.CSS_SELECTOR, "slot")
        # logging.info("✅ Slot en vaadin-horizontal-layout encontrado.")

        # Acceder al elemento 'vertical-toolbar' dentro del slot
        vertical_toolbar = driver.execute_script(
            "return arguments[0].assignedElements()[1];", slot_horizontal  # Cambiar índice si es necesario
        )
        # logging.info("✅ vertical-toolbar encontrado.")

        # Buscar el contenedor de botones dentro del shadow root
        t_vertical_toolbar = vertical_toolbar.find_element(By.CSS_SELECTOR, ".t-vertical-toolbar")
        # logging.info("✅ t-vertical-toolbar encontrado.")

        # Buscar el botón de descarga
        boton_descarga = t_vertical_toolbar.find_element(By.CSS_SELECTOR, "paper-icon-button.btn-back")

        # Hacer scroll hasta el botón y hacer clic
        driver.execute_script("arguments[0].scrollIntoView();", boton_descarga)
        time.sleep(1)  # Pequeña espera para evitar problemas de renderizado
        boton_descarga.click()
        logging.info("✅ Se hizo clic en el botón de volver.")

    except Exception as e:
        logging.error(f"Error al interactuar con el botón dentro del iframe: {e}")
        driver.switch_to.default_content() 

def descargar_detalle(driver):
        # Esperar a que aparezca el 'vaadin-context-menu-overlay'
    vaadin_menu_overlay = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-context-menu-overlay#overlay"))
    )
    # logging.info("✅ vaadin-context-menu-overlay encontrado.")

    # Obtener el shadow root de 'vaadin-context-menu-overlay'
    shadow_root_menu = driver.execute_script("return arguments[0].shadowRoot", vaadin_menu_overlay)
    # logging.info("✅ shadow_root_menu encontrado.")

    slot_element_1 = shadow_root_menu.find_element(By.CSS_SELECTOR, "div#content slot")
    # logging.info("✅ Slot dentro de shadow_root_menu encontrado.")

    # Obtener el primer elemento asignado dentro del slot, que es 'vaadin-context-menu-list-box'
    vaadin_context_menu_list_box = driver.execute_script(
        "return arguments[0].assignedElements()[0];", slot_element_1
    )
    # logging.info("✅ vaadin-context-menu-list-box encontrado.")

    shadow_root_list_box = driver.execute_script("return arguments[0].shadowRoot", vaadin_context_menu_list_box)
    # logging.info("✅ shadow_root_list_box encontrado.")

    # Obtener el slot dentro del shadow root de vaadin-context-menu-list-box
    slot_item = shadow_root_list_box.find_element(By.CSS_SELECTOR, "slot")
    # logging.info("✅ Slot dentro de vaadin-context-menu-list-box encontrado.")

    vaadin_context_menu_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-context-menu-item.vaadin-menu-item"))
    )
    # logging.info("✅ vaadin-context-menu-item encontrado.")

    # Obtener el shadow root de 'vaadin-context-menu-item'
    shadow_root_item = driver.execute_script("return arguments[0].shadowRoot", vaadin_context_menu_item)
    # logging.info("✅ shadow_root_item encontrado.")

    # Obtener el slot dentro del shadow root de vaadin-context-menu-item
    slot_button = shadow_root_item.find_element(By.CSS_SELECTOR, "slot")
    # logging.info("✅ Slot dentro de vaadin-context-menu-item encontrado.")

    # Obtener el primer elemento asignado dentro del slot, que es 'vaadin-button'
    vaadin_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-button.link-button"))
    )
    # logging.info("✅ vaadin-button encontrado.")

    # Obtener el shadow root de 'vaadin-button'
    shadow_root_button = driver.execute_script("return arguments[0].shadowRoot", vaadin_button)
    # logging.info("✅ shadow_root_button encontrado.")

    # Ahora acceder al botón dentro del shadow root
    button = shadow_root_button.find_element(By.CSS_SELECTOR, "button#button")
    # logging.info("✅ Botón encontrado dentro del shadow root de vaadin-button.")

    # Hacer clic en el botón
    button.click()
    logging.info("✅ Se hizo clic en el botón.")
    time.sleep(2)

def clickear_boton_confirmacion(driver):
    vaadin_vertical_layout_descarga = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-vertical-layout.no-margin.bbr-app"))
    )
    # logging.info("✅ vaadin-vertical-layout encontrado.")

    # 2Obtener el shadow root de 'vaadin-vertical-layout'
    shadow_root_vertical_descarga = driver.execute_script("return arguments[0].shadowRoot", vaadin_vertical_layout_descarga)
    # logging.info("✅ shadow_root de vaadin-vertical-layout encontrado.")

    # Acceder al 'slot' y verificar elementos asignados
    slot_element = shadow_root_vertical_descarga.find_element(By.CSS_SELECTOR, "slot")
    # logging.info("✅ Slot encontrado en vaadin-vertical-layout.")

    assigned_elements = driver.execute_script("return arguments[0].assignedElements();", slot_element)
    if assigned_elements and len(assigned_elements) > 0:
        app_box = assigned_elements[0]  # Primer elemento debe ser app-box
        # logging.info("✅ app-box encontrado.")
    else:
        logging.error("❌ No se encontraron elementos dentro del slot.")
        # raise Exception("No se encontraron elementos en el slot de vaadin-vertical-layout")

    # Obtener el shadow root de 'app-box'
    shadow_root_app_box = driver.execute_script("return arguments[0].shadowRoot", app_box)
    # logging.info("✅ shadow_root de app-box encontrado.")

    # Acceder a 'contentContainer' dentro de app-box
    content_container = shadow_root_app_box.find_element(By.CSS_SELECTOR, "#contentContainer")
    # logging.info("✅ contentContainer encontrado en app-box.")

    # Acceder al slot dentro de contentContainer
    slot_app_box = content_container.find_element(By.CSS_SELECTOR, "slot")
    # logging.info("✅ Slot encontrado en contentContainer.")

    assigned_drawers = driver.execute_script("return arguments[0].assignedElements();", slot_app_box)
    if assigned_drawers and len(assigned_drawers) > 0:
        app_drawer = assigned_drawers[0]  # Primer app-drawer
        # logging.info("✅ Primer app-drawer encontrado.")
    else:
        # logging.error("❌ No se encontraron app-drawers dentro del slot.")
        raise Exception("No se encontraron app-drawers en el slot de contentContainer")

    # Obtener el shadow root de 'app-drawer'
    shadow_root_app_drawer = driver.execute_script("return arguments[0].shadowRoot", app_drawer)
    # logging.info("✅ shadow_root de app-drawer encontrado.")

    # Acceder al slot dentro del shadow root de app-drawer
    slot_app_drawer = shadow_root_app_drawer.find_element(By.CSS_SELECTOR, "slot")
    # logging.info("✅ Slot encontrado en app-drawer.")

    assigned_divs = driver.execute_script("return arguments[0].assignedElements();", slot_app_drawer)
    if assigned_divs and len(assigned_divs) > 0:
        div_element = assigned_divs[0]  # Único div dentro del slot
        # logging.info("✅ Div dentro del slot de app-drawer encontrado.")
    else:
        # logging.error("❌ No se encontró ningún div dentro del slot de app-drawer.")
        raise Exception("No se encontró el div dentro del slot de app-drawer")
    
    filter_details_layout = div_element.find_element(By.CSS_SELECTOR, "vaadin-vertical-layout.no-margin.bbr-filter-details.bbr-section")
    # logging.info("✅ vaadin-vertical-layout (bbr-filter-details) encontrado.")

    # Obtener el shadow root del vaadin-vertical-layout (bbr-filter-details)
    shadow_root_filter_details = driver.execute_script("return arguments[0].shadowRoot", filter_details_layout)
    # logging.info("✅ shadow_root del vaadin-vertical-layout (bbr-filter-details) encontrado.")

    # Dentro del shadow root, acceder al slot y obtener el primer elemento asignado, que es el vaadin-horizontal-layout
    slot_filter_details = shadow_root_filter_details.find_element(By.CSS_SELECTOR, "slot")
    # logging.info("✅ Slot encontrado en vaadin-vertical-layout (bbr-filter-details).")

    vaadin_horizontal_layout_filter = driver.execute_script("return arguments[0].assignedElements()[0];", slot_filter_details)
    # logging.info("✅ vaadin-horizontal-layout obtenido desde el slot de vaadin-vertical-layout (bbr-filter-details).")

    #  Obtener el shadow root del vaadin-horizontal-layout (filter-header-toolbar)
    shadow_root_hl = driver.execute_script("return arguments[0].shadowRoot", vaadin_horizontal_layout_filter)
    # logging.info("✅ shadow_root del vaadin-horizontal-layout (filter-header-toolbar) encontrado.")

    #  Dentro del shadow root del vaadin-horizontal-layout, acceder al slot y obtener el primer elemento asignado, que es un vaadin-vertical-layout
    slot_hl = shadow_root_hl.find_element(By.CSS_SELECTOR, "slot")
    # logging.info("✅ Slot encontrado en vaadin-horizontal-layout (filter-header-toolbar).")

    vaadin_vertical_layout_in_hl = driver.execute_script("return arguments[0].assignedElements()[0];", slot_hl)
    # logging.info("✅ vaadin-vertical-layout encontrado dentro del slot de vaadin-horizontal-layout.")

    # Obtener el shadow root del vaadin-vertical-layout (el que tiene theme="spacing")
    shadow_root_vl = driver.execute_script("return arguments[0].shadowRoot", vaadin_vertical_layout_in_hl)
    # logging.info("✅ shadow_root del vaadin-vertical-layout (theme=spacing) encontrado.")

    #  Dentro del shadow root de este vaadin-vertical-layout, acceder al slot y obtener el primer elemento asignado, que es el vaadin-button
    slot_vl = shadow_root_vl.find_element(By.CSS_SELECTOR, "slot")
    # logging.info("✅ Slot encontrado en vaadin-vertical-layout (theme=spacing).")

    vaadin_button = driver.execute_script("return arguments[0].assignedElements()[0];", slot_vl)
    # logging.info("✅ vaadin-button encontrado dentro del slot de vaadin-vertical-layout (theme=spacing).")

    # Esperar a que aparezca el vaadin-button con la clase "filter-apply-button"
    filter_apply_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-button.filter-apply-button"))
    )
    # logging.info("✅ vaadin-button (filter-apply-button) encontrado.")

    # Obtener el shadow root del vaadin-button
    shadow_root_filter_apply = driver.execute_script("return arguments[0].shadowRoot", filter_apply_button)
    # logging.info("✅ shadow_root del vaadin-button (filter-apply-button) encontrado.")

    # Dentro del shadow root, buscar el botón con id "button"
    final_button = shadow_root_filter_apply.find_element(By.CSS_SELECTOR, "button#button")
    # logging.info("✅ Botón encontrado dentro del shadow root de vaadin-button.")

    # Hacer clic en el botón
    final_button.click()
    logging.info("✅ Se hizo clic en el botón final.")
    time.sleep(5)   

def esperar_descarga(nombre_archivo, carpeta_descargas, timeout=30):
    ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)
    tiempo_inicial = time.time()
    
    while not os.path.exists(ruta_completa):
        if time.time() - tiempo_inicial > timeout:
            print(f"❌ Tiempo de espera agotado. No se encontró el archivo: {ruta_completa}")
            return None
        time.sleep(1)  # Espera un segundo antes de verificar de nuevo
    
    print(f"✅ Archivo encontrado: {ruta_completa}")
    return ruta_completa  # Retorna la ruta completa del archivo

def clickear_archivo_xlsx(driver):
    # Esperar a que aparezca el  vaadin-notification-container
    vaadin_notification_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="vaadin-notification-card"]/flow-component-renderer/div/vaadin-horizontal-layout/div/vaadin-vertical-layout/vaadin-horizontal-layout/a'))
    )
    # logging.info("✅ vaadin-notification-container XPATH encontrado.")
    time.sleep(1)

    nombre_archivo = vaadin_notification_container.text.strip()
    # logging.info(f"✅ Nombre del archivo obtenido: {nombre_archivo}")

    vaadin_notification_container.click()
    # logging.info("✅ Se hizo clic en vaadin-notification-container.")

    # Obtener el shadow root del vaadin-notification-container
    shadow_root_notification = driver.execute_script("return arguments[0].shadowRoot", vaadin_notification_container)
    # logging.info("✅ shadow_root de vaadin-notification-container encontrado.")

    return nombre_archivo

def modificar_excel(nombre_archivo, carpeta_descargas, sku_value, nombre_columna="Fecha"):
    try:
        # Obtener la fecha de ayer en el formato requerido
        fecha_ayer = (datetime.today() - timedelta(days=1)).strftime("%d-%m-%Y")

        # Esperar a que el archivo se descargue
        ruta_completa = esperar_descarga(nombre_archivo, carpeta_descargas)
        if not ruta_completa:
            return  # Si el archivo no se encuentra, salir de la función

        # Cargar el archivo Excel
        df = pd.read_excel(ruta_completa)

        # Agregar la nueva columna con la fecha de ayer
        df[nombre_columna] = fecha_ayer  

        df["SKU"] = sku_value

        df["Descripcion"] = None

        df["Cadena"] = "CRUZ VERDE"

        df = df.rename(columns={
            "Cód. local": "N° Local",  # Cambia "Producto" a "Nombre del Producto"
            "Venta (un)": "Unidades",        # Cambia "Precio" a "Valor Unitario"
            "Venta a costo (s/iva)": "Venta",      # Cambia "Fecha" a "Fecha de Registro"
        })

        # Guardar el archivo modificado
        df.to_excel(ruta_completa, index=False)  # Sobrescribe el archivo original
        print(f"✅ Se agregó la columna '{nombre_columna}' con la fecha '{fecha_ayer}' y la columna 'SKU' con el valor '{sku_value}' correctamente en '{ruta_completa}'.")

    except Exception as e:
        print(f"❌ Error modificando el Excel '{nombre_archivo}': {e}")

def es_pagina_login(driver):
    # URL de la página de login
    url_login = "https://ssofemsa.bbr.cl/auth/realms/femsa/protocol/openid-connect/auth"
    
    # Verificar si la URL actual contiene la URL de login
    return url_login in driver.current_url

def hacer_click_en_label(driver):
    try:
        # Esperar a que la tabla (vaadin-grid-pro) esté presente
        vaadin_grid = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-grid-pro.bbr-grid"))
        )
        # logging.info("✅ Grid encontrado correctamente.")

        # Acceder al shadow root del grid
        shadow_root_grid = driver.execute_script("return arguments[0].shadowRoot", vaadin_grid)
        # logging.info("✅ shadow_root_grid encontrado correctamente.")

        # Esperar a que las celdas del primer producto (slot con id "vaadin-grid-cell-content-30") se carguen
        WebDriverWait(driver, 10).until(
            lambda d: len(shadow_root_grid.find_elements(By.NAME, "vaadin-grid-cell-content-30")) > 0
        )
        logging.info("✅ Celdas cargadas.")

        cell_id = 30  # Primer identificador de slot
        while True:
            # Construir el selector para el slot actual
            selector = f'td[first-column] slot[name="vaadin-grid-cell-content-{cell_id}"]'
            filas = shadow_root_grid.find_elements(By.CSS_SELECTOR, selector)
            
            # Si no se encuentran elementos para el id actual, se asume que no hay más productos
            if not filas:
                logging.info("No se ha encontrado mas productos.")
                break

            logging.info(f"🔍 Filas encontradas en primera columna con id {cell_id}: {len(filas)}")

            for slot in filas:
                try:
                    # Obtener el contenido asignado al slot
                    contenido_slot = driver.execute_script("return arguments[0].assignedNodes()", slot)
                    # logging.info(f"🔍 Contenido del slot: {len(contenido_slot)}")
                    
                    for nodo in contenido_slot:
                        try:
                            div_objetivo = nodo.find_element(By.CSS_SELECTOR, "div.bbr-column-action")
                            logging.info(f"🔍 Se encontró el div.bbr-column-action correctamente: {div_objetivo.text}")
                            
                            driver.execute_script("arguments[0].scrollIntoView();", div_objetivo)
                            div_objetivo.click()
                            sku_value = div_objetivo.text  # Almacenar el valor del SKU
                            logging.info(f"✅ Se hizo clic en el número: {sku_value}")

                            # Se mantiene la estructura actual de métodos después del click
                            try:
                                carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
                                descargar_archivo(driver)
                                salir_iframe(driver)
                                entrar_iframe(driver)
                                descargar_detalle(driver)
                                salir_iframe(driver)
                                entrar_iframe(driver)
                                clickear_boton_confirmacion(driver)
                                salir_iframe(driver)
                                nombre_archivo = clickear_archivo_xlsx(driver)
                                modificar_excel(nombre_archivo, carpeta_descargas, sku_value)
                                entrar_iframe(driver)
                                clickear_en_volver(driver)
  
                                time.sleep(3)
                            except Exception as e:
                                logging.error(f"❌ Error al hacer clic en el botón de descarga: {e}")
                                
                                time.sleep(2)
                                # Una vez procesado el primer nodo que cumple la condición en este slot, se sale del bucle
                                break
                        except Exception:
                            continue  # Si el nodo no tiene el div, se pasa al siguiente
                except Exception as e:
                    logging.warning(f"⚠ No se pudo hacer clic en una celda: {e}")

            # Incrementar el identificador en 7 para buscar el siguiente producto
            cell_id += 7

    except Exception as e:
        logging.error(f"❌ Error en el proceso: {e}")

def extract_info():

    # Configurar las opciones de ChromeDriver
    print("Configurando driver")

    service = Service("C:/Users/diego/Documents/instalables/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    chrome_options = Options()
    # chrome_options.add_argument("--headless") #Deshabilita qque se abra una ventana de navegador
    chrome_options.add_argument("--disable-gpu")  # Deshabilitar aceleración de gráficos
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--dns-prefetch-disable")
    driver = webdriver.Chrome(options = chrome_options, service=service)
    # Abrir la página

    #       driver.get('https://femsab2b.bbr.cl/SaludCL/BBRe-commerce/main')

    try:
        
        hacer_login(driver)
        max_reintentos = 3
        reintentos = 0

        while reintentos < max_reintentos:
            try:
                # Realizar la navegación inicial
                if realizar_navegacion(driver):
                    # Verificar si se redirigió a la página de login después de la navegación
                    if es_pagina_login(driver):
                        reintentos += 1
                        logging.warning(f"⚠️ Se redirigió a la página de login. Reintento {reintentos}/{max_reintentos}...")

                        # Volver a hacer login
                        if hacer_login(driver):
                            continue  # Volver a intentar la navegación
                        else:
                            logging.error("❌ No se pudo realizar el login. Deteniendo el proceso.")
                            break
                    else:
                        # Si no hay redirección, salir del bucle
                        break
                else:
                    logging.error("❌ Error durante la navegación inicial. Deteniendo el proceso.")
                    break

            except Exception as e:
                logging.error(f"Error en el flujo principal: {e}")
                break

        # Continuar con el resto del proceso si no se alcanzó el límite de reintentos
        if reintentos < max_reintentos:
            entrar_iframe(driver)
            modificar_filtro_fecha_dentro_iframe(driver)
            time.sleep(1)
            interactuar_con_boton_dentro_iframe(driver)
            time.sleep(2)
            hacer_click_en_label(driver)
            time.sleep(2)
        else:
            logging.error("❌ Se alcanzó el límite de reintentos. No se pudo continuar.")

    except Exception as e:
        logging.error(f"Error al interactuar con el inicio de sesión: {e}")

if __name__ == "__main__":
    start_time = time.time()
    print(start_time)

    extract_info()  # Llamada a la función sin desempacar

    print("Tiempo transcurrido:", tiempo_transcurrido(time.time() - start_time))