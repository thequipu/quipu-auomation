# pages/schema_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class SchemaPage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

        # menu + page
        self.hamburger = (By.ID, "page-menu")
        self.schema_menu = (By.ID, "Schema-page")

        # add new form (match your working IDs)
        self.add_btn = (By.ID, "add-schema-btn")
        self.name_inp = (By.ID, "schemaName")
        self.prefix_inp = (By.ID, "schema-prefix")
        self.desc_inp = (By.ID, "schema-description")
        self.create_btn = (By.ID, "create-schema")          # you used this in your script

        # side panel selectors
        self.typeahead = (By.ID, "typeahead-focus")
        self.select_all = (By.ID, "select-all-btn")
        self.done_btn = (By.ID, "done-btn")

    def open_menu(self):
        self.wait.until(EC.element_to_be_clickable(self.hamburger)).click()
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable(self.schema_menu)).click()
        time.sleep(2)

    def start_add_new(self):
        self.wait.until(EC.element_to_be_clickable(self.add_btn)).click()
        time.sleep(2)

    def fill_basic_details(self, name, prefix, description):
        self.wait.until(EC.element_to_be_clickable(self.name_inp)).send_keys(name)
        self.wait.until(EC.element_to_be_clickable(self.prefix_inp)).send_keys(prefix)
        self.wait.until(EC.element_to_be_clickable(self.desc_inp)).send_keys(description)

    def create_schema_open_builder(self):
        self.wait.until(EC.element_to_be_clickable(self.create_btn)).click()

    def attach_tables_from_typeahead(self, term: str):
        box = self.wait.until(EC.presence_of_element_located(self.typeahead))
        box.send_keys(term)
        time.sleep(3)  # preserve your successful timing
        box.send_keys(Keys.ENTER)
        # side panel actions
        self.wait.until(EC.element_to_be_clickable(self.select_all)).click()
        self.wait.until(EC.element_to_be_clickable(self.done_btn)).click()