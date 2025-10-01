from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class FabricPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open_real_world_datamart(self):
        fabric_menu = self.wait.until(EC.element_to_be_clickable((By.ID, "fabric-menu")))
        fabric_menu.click()
        option = self.wait.until(EC.element_to_be_clickable((By.ID, "RealWorldDataMart-fabric")))
        option.click()
        time.sleep(3)  # buffer to ensure page loads