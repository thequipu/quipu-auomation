from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DataCatalogPage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open_menu(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "page-menu"))).click()
        time.sleep(0.5)
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "Data Catalog-page"))).click()
        except Exception:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Data Catalog']"))).click()
        time.sleep(1)

    def show_data_sources(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "show-ds-btn"))).click()
        time.sleep(1)

    def open_data_source(self, name_id_or_text):
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, name_id_or_text))).click()
            return
        except Exception:
            pass
        xpath = f"//button[.//span[normalize-space()='{name_id_or_text}'] or normalize-space()='{name_id_or_text}']"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def edit_description(self, new_text):
        self.wait.until(EC.element_to_be_clickable((By.ID, "edit-ds-btn"))).click()
        ta = self.wait.until(EC.presence_of_element_located((By.ID, "taDescription")))
        try: ta.clear()
        except Exception: pass
        ta.send_keys(new_text)
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "save-ds-btn"))).click()
        except Exception:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Save']"))).click()
        time.sleep(1)

    def read_description(self):
        ta = self.wait.until(EC.presence_of_element_located((By.ID, "taDescription")))
        return ta.get_attribute("value") or ta.text