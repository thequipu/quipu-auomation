# pages/schema_page.py
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# Optional screenshot helper if you have it
try:
    from utils.screenshots import take_screenshot
except Exception:
    def take_screenshot(driver, name):  # no-op fallback
        os.makedirs("artifacts/screenshots", exist_ok=True)
        driver.save_screenshot(os.path.join("artifacts/screenshots", f"{name}.png"))

class SchemaPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # ---------- Navigation ----------
    def open_menu(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "page-menu"))).click()
        time.sleep(1)

    def goto_schema(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "Schema-page"))).click()
        time.sleep(1)

    def open_schema_by_id(self, schema_id: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, schema_id))).click()
        time.sleep(1)

    def back_to_workspace(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "back-to-schema-workspace-page"))).click()

    def back_to_schema_list(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "back-to-schema-page"))).click()

    # ---------- Canvas + Toolbar ----------
    def zoom_out_double(self):
        el = self.driver.find_element(By.ID, "graph-zoom-out-btn")
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).double_click(el).perform()

    def zoom_in_double(self):
        el = self.driver.find_element(By.ID, "graph-zoom-in-btn")
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).double_click(el).perform()

    def fit_to_screen(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "graph-fit-to-screen-btn"))).click()
        time.sleep(0.3)

    # ---------- Node config panel ----------
    def open_node_config_panel(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "nodeConfigPanel-btn"))).click()

    def open_node_configuration(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "node-configuration"))).click()

    def back_from_node_config(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "Go back to Node Config Panel"))).click()

    # ---------- Edit schema dialog ----------
    def click_edit_schema_toolbar(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "edit-schema-btn"))).click()

    def open_similarity_view(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "similarityView-btn"))).click()

    def edit_schema_by_tile(self, tile_edit_id: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, tile_edit_id))).click()

    def set_schema_description(self, text: str):
        desc = self.wait.until(EC.presence_of_element_located((By.ID, "taDescription")))
        desc.send_keys(text)

    def toggle_versions_accordion(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "ngb-accordion-item-1-toggle"))).click()

    def save_schema_dialog(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "save-schema"))).click()

    def close_schema_dialog(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "schema-dialog-back"))).click()

    # ---------- “Add New Schema” flow ----------
    def open_add_new_schema(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "add-schema-btn"))).click()

    def fill_new_schema_form(self, name: str, prefix: str, description: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, "schemaName"))).send_keys(name)
        self.wait.until(EC.element_to_be_clickable((By.ID, "schema-prefix"))).send_keys(prefix)
        self.wait.until(EC.element_to_be_clickable((By.ID, "schema-description"))).send_keys(description)

    def create_schema_open_workspace(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "create-schema"))).click()

    def search_datasource_in_typeahead(self, text: str, press_enter=True):
        box = self.wait.until(EC.presence_of_element_located((By.ID, "typeahead-focus")))
        box.send_keys(text)
        time.sleep(1.5)
        if press_enter:
            box.send_keys(Keys.ENTER)

    def select_all_sources_in_sidepanel(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "select-all-btn"))).click()

    def sidepanel_done(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "done-btn"))).click()

    # ---------- Create Version tab ----------
    def open_create_version_tab(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "mat-tab-label-0-1"))).click()

    def select_schema_in_create_version(self, schema_option_id: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, "mat-select-16"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, schema_option_id))).click()

    def select_version_in_create_version(self, version_option_id: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, "schema-version-select"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, version_option_id))).click()

    def fill_create_version_names(self, new_schema_name: str, new_desc: str, version_desc: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, "new-schema"))).send_keys(new_schema_name)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.6)
        self.wait.until(EC.element_to_be_clickable((By.ID, "mat-input-6"))).send_keys(new_desc)
        # there is a typo in the original id; keep as-is because it’s from your script
        self.wait.until(EC.element_to_be_clickable((By.ID, "camat-input-7"))).send_keys(version_desc)

    def create_version_submit(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "create-schema"))).click()

    # ---------- Utility ----------
    def screenshot(self, name: str):
        take_screenshot(self.driver, name)