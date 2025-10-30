from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SchemaPage:
    def __init__(self, driver, wait=None):
        self.driver = driver
        self.wait = wait

    def open_menu(self):
        self.driver.find_element(By.ID, "page-menu").click()

    def open_schema_page(self):
        self.driver.find_element(By.ID, "Schema-page").click()

    def click_add_new(self):
        self.driver.find_element(By.ID, "add-schema-btn").click()

    def fill_schema_details(self, name, prefix, desc):
        self.driver.find_element(By.ID, "schemaName").send_keys(name)
        self.driver.find_element(By.ID, "schema-prefix").send_keys(prefix)
        self.driver.find_element(By.ID, "schema-description").send_keys(desc)
        self.driver.find_element(By.ID, "create-schema").click()

    def typeahead_and_select(self, text):
        inp = self.driver.find_element(By.ID, "typeahead-focus")
        inp.send_keys(text)
        # ENTER happens in tests when needed