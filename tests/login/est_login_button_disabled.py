import json
from selenium.webdriver.common.by import By
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage

def test_login_button_disabled():
    config = DriverFactory.load_config("config/config.json")
    driver, wait = DriverFactory.get_driver()
    try:
        lp = LoginPage(driver)
        lp.open(config["base_url"])
        lp.enter_tenant(config["tenant"])
        lp.click_proceed()
        login_button = driver.find_element(By.ID, "signIn-btn")
        assert not login_button.is_enabled()
    finally:
        driver.quit()