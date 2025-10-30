from selenium.webdriver.common.by import By

class FabricPage:
    def __init__(self, driver):
        self.driver = driver

    def open_menu(self):
        self.driver.find_element(By.ID, "page-menu").click()

    def open_fabric(self):
        self.driver.find_element(By.ID, "Hetionet-Data_fabric").click()