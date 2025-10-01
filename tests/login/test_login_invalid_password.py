import json
import time
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from utils.screenshot import take_screenshot
from selenium.webdriver.common.by import By

def test_login_invalid_password():
    with open("config/config.json") as f:
        config = json.load(f)

    driver, wait = DriverFactory.get_driver()
    login_page = LoginPage(driver)

    login_page.open(config["base_url"])
    login_page.enter_tenant(config["tenant"])
    login_page.click_proceed()
    login_page.enter_username(config["username"])
    login_page.enter_password("wrongpass")
    login_page.click_login()

    time.sleep(2)
    take_screenshot(driver, "password")
    time.sleep(5)
    driver.quit()