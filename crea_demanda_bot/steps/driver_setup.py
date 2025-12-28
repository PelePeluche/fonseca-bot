# File: setup_driver.py

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    scale_factor = float(os.getenv("CHROME_SCALE_FACTOR", "0.75"))
    options = Options()
    options.add_argument(f"--force-device-scale-factor={scale_factor}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver
