from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class SearchPage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open_fabric(self, fabric_id="Hetionet-fabric"):
        self.wait.until(EC.element_to_be_clickable((By.ID, "fabric-menu"))).click()
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, fabric_id))).click()
        except Exception:
            name = fabric_id.replace("-fabric", "")
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//span[normalize-space()='{name}']/ancestor::button"))).click()
        time.sleep(1)

    def search(self, text):
        try:
            box = self.wait.until(EC.presence_of_element_located((By.ID, "search-input")))
        except Exception:
            box = self.wait.until(EC.presence_of_element_located((By.ID, "search-node-input")))
        box.clear()
        box.send_keys(text)
        box.send_keys(Keys.ENTER)
        time.sleep(2)

    def switch_to_table_view(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "tableView-btn"))).click()
        except Exception:
            self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Table View']"))).click()
        time.sleep(1)

    def click_next(self):
        locators = [
            (By.ID, "next-btn"),
            (By.CSS_SELECTOR, "button[aria-label='Next'], button.mat-paginator-navigation-next"),
            (By.XPATH, "//button[.//span[normalize-space()='Next'] or normalize-space()='Next']")
        ]
        last = None
        for by, sel in locators:
            try:
                self.wait.until(EC.element_to_be_clickable((by, sel))).click()
                return
            except Exception as e:
                last = e
        raise last