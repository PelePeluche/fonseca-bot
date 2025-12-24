# File: manage_tabs.py

def open_new_tab(driver):
    driver.execute_script(
        "window.open('https://www.justiciacordoba.gob.ar/PresentacionDemandas/Menu/Default.aspx', '_blank');"
    )
    driver.switch_to.window(driver.window_handles[-1])
