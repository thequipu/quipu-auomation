# pages/search_config_page.py
import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SearchConfigPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # ---------- Navigation ----------
    def open_menu(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "page-menu"))).click()
        time.sleep(1)

    def goto_search_configuration(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "Search Configuration-page"))).click()
        time.sleep(2)

    # ---------- Fabric selection ----------
    def open_fabric_dropdown(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "fabric-dropdown"))).click()
        time.sleep(0.5)

    def select_fabric_by_id(self, fabric_id: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, fabric_id))).click()
        time.sleep(1)

    # ---------- Entity / section selection ----------
    def open_entity_section(self, entity_id: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, entity_id))).click()
        time.sleep(0.5)

    def toggle_checkboxes_by_ids(self, ids: List[str], pause: float = 0.5):
        for cid in ids:
            el = self.wait.until(EC.element_to_be_clickable((By.ID, cid)))
            el.click()
            time.sleep(pause)

    def click_save_for_entity(self, save_btn_id: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, save_btn_id))).click()
        time.sleep(0.7)

    # ---------- Corporation path / E360 ----------
    def open_corporation_query_header(self):
        # Uses your original XPath
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="innerAccordion1"]/div[1]/h2/div'))
        ).click()
        time.sleep(0.7)

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.2)

    def save_e360_path(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "save-e360-path-btn"))).click()
        time.sleep(0.7)

    def close_e360_path(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "close-e360-path-btn"))).click()
        time.sleep(0.7)