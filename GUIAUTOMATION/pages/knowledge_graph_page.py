# pages/knowledge_graph_page.py
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class KnowledgeGraphPage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.actions = ActionChains(driver)
        self.hamburger = (By.ID, "page-menu")
        self.kg_menu   = (By.ID, "Knowledge Graph-page")

        # Labels
        self.labels_css = (By.CSS_SELECTOR, "button[id^='label-']")

        # Relationships (scoped to the “Relationships” side-block)
        self.relationships_xpath = (
            By.XPATH,
            "//h6[normalize-space()='Relationships']"
            "/following-sibling::div[contains(@class,'labels-row')]"
            "//button[starts-with(@id,'rel-')]"
        )

    def open(self):
        self.wait.until(EC.element_to_be_clickable(self.hamburger)).click()
        self.wait.until(EC.element_to_be_clickable(self.kg_menu)).click()
        # Wait for either labels or relationships to be present
        self.wait.until(
            EC.any_of(
                EC.presence_of_element_located(self.labels_css),
                EC.presence_of_element_located(self.relationships_xpath),
            )
        )

    # -------- LABELS (unchanged) ----------
    def get_labels_with_tooltips(self):
        elems = self.driver.find_elements(*self.labels_css)
        data = []
        for el in elems:
            self.actions.move_to_element(el).perform()
            data.append({
                "Label": (el.text or "").strip(),
                "Tooltip": (el.get_attribute("title") or "").strip()
            })
        return data

    def export_labels_to_csv(self, filepath):
        rows = self.get_labels_with_tooltips()
        import os; os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["Label", "Tooltip"])
            w.writeheader(); w.writerows(rows)
        return filepath

    def read_labels_from_csv(self, filepath):
        with open(filepath, newline="", encoding="utf-8") as f:
            return [row for row in csv.DictReader(f)]

    # -------- RELATIONSHIPS (new) ----------
    def get_relationships_with_tooltips(self):
        # If the section isn’t present, return an empty list gracefully
        elems = self.driver.find_elements(*self.relationships_xpath)
        data = []
        for el in elems:
            self.actions.move_to_element(el).perform()
            data.append({
                "Relationship": (el.text or "").strip(),
                "Tooltip": (el.get_attribute("title") or "").strip()
            })
        return data

    def export_relationships_to_csv(self, filepath):
        rows = self.get_relationships_with_tooltips()
        import os; os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["Relationship", "Tooltip"])
            w.writeheader(); w.writerows(rows)
        return filepath

    def read_relationships_from_csv(self, filepath):
        with open(filepath, newline="", encoding="utf-8") as f:
            return [row for row in csv.DictReader(f)]