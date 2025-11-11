# GUIAUTOMATION/pages/document_linker_page.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

class DocumentLinkerPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open_menu(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "page-menu"))).click()
        time.sleep(1)

    def goto_document_linker(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "Document Linker-page"))).click()
        time.sleep(2)

    def open_extract_dialog(self):
        self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "/html/body/app-root/app-document-visualizer/main/div/div/div[2]/button"
        ))).click()
        time.sleep(1)

    def select_slinker_by_index(self, index_zero_based):
        select_el = self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "/html/body/app-root/app-document-visualizer/main/div/div[2]/div/form/div[1]/select"
        )))
        Select(select_el).select_by_index(index_zero_based)
        time.sleep(1)

    def select_datasource_by_index(self, index_zero_based):
        select_el = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "body > app-root > app-document-visualizer > main > div > div.overlay.ng-star-inserted > div > form > div:nth-child(3) > select"
        )))
        Select(select_el).select_by_index(index_zero_based)
        time.sleep(1)

    def click_extract(self):
        self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "body > app-root > app-document-visualizer > main > div > div.overlay.ng-star-inserted > div > form > div.mt-3.d-flex.justify-content-end > button.btn.btn-primary.me-2"
        ))).click()
        time.sleep(1)

    def cancel_if_needed(self):
        try:
            self.wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                "body > app-root > app-document-visualizer > main > div > div.overlay.ng-star-inserted > div > form > div.mt-3.d-flex.justify-content-end > button.btn.btn-outline-primary"
            ))).click()
            time.sleep(1)
        except TimeoutException:
            pass