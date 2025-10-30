from selenium.webdriver.common.by import By

class SearchPage:
    def __init__(self, driver):
        self.driver = driver

    def search_text(self, text):
        box = self.driver.find_element(By.ID, "search-input")
        box.clear(); box.send_keys(text)