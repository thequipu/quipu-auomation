import json
import time
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from utils.screenshot import take_screenshot

def test_login_button_disabled():
    with open("config/config.json") as f:
        config = json.load(f)

    driver,wait = DriverFactory.get_driver()
    login_page = LoginPage(driver)

    login_page.open(config["base_url"])
    login_page.enter_tenant(config["tenant"])
    login_page.click_proceed()

    login_button = driver.find_element(By.ID, "signIn-btn")
    assert not login_button.is_enabled()

    take_screenshot(driver, "222")
    time.sleep(5)

    driver.quit()