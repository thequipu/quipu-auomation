import json
import pytest
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="session")
def config():
    with open("config/config.json") as f:
        return json.load(f)

@pytest.fixture(scope="function")
def driver():
    driver,wait = DriverFactory.get_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def login(driver, config):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.enter_tenant(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password(config["password"])
    lp.click_login()
    # extra safety: ensure post-login element is visible
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "fabric-menu")))
    return driver