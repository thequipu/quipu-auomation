from selenium.webdriver.common.by import By

class DataCatalogPage:
    def __init__(self, driver):
        self.driver = driver

    def open_menu(self):
        self.driver.find_element(By.ID, "page-menu").click()

    def open_datacatalog(self):
        self.driver.find_element(By.ID, "Data Catalog-page").click()