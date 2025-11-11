from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find_element(self, locator):
        """Find a single element"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator):
        """Wait for element to be clickable and click it"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def enter_text(self, locator, text):
        """Enter text into an input field"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        return element

    def press_enter(self, locator):
        """Press Enter key on an element"""
        element = self.find_element(locator)
        element.send_keys(Keys.ENTER)

    def wait_and_click(self, locator, sleep_after=0):
        """Click element and optionally sleep after"""
        self.click_element(locator)
        if sleep_after > 0:
            time.sleep(sleep_after)

    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url

    def maximize_window(self):
        """Maximize browser window"""
        self.driver.maximize_window()