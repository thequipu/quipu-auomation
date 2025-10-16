from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class FabricPage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open_menu(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "fabric-menu"))).click()
        time.sleep(1)

    def open_real_world_datamart(self):
        self.open_menu()
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "RealWorldDataMart-fabric"))).click()
        except Exception:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='RealWorldDataMart']/ancestor::button"))).click()
        time.sleep(1)

    def open_hetionet(self):
        self.open_menu()
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "Hetionet-fabric"))).click()
        except Exception:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Hetionet']/ancestor::button"))).click()
        time.sleep(1)