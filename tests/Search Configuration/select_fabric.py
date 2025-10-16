# tests/Search Configuration/select_fabric.py
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from utils.screenshot import take_screenshot


def test_select_fabric():
    # load config
    with open("config/config.json") as f:
        config = json.load(f)

    # driver + wait (matches your current DriverFactory.get_driver() return)
    driver, wait = DriverFactory.get_driver()

    # ---- login ----
    login = LoginPage(driver)
    login.open(config["base_url"])
    login.enter_tenant(config["tenant"])
    login.click_proceed()
    login.enter_username(config["username"])
    login.enter_password(config["password"])
    login.click_login()

    # ---- navigate to Fabric ----
    fabric_menu = wait.until(EC.element_to_be_clickable((By.ID, "fabric-menu")))
    fabric_menu.click()

    # choose which Fabric to open (pick one below or change the id)
    # Known options in your project:
    #   - "Hetionet-fabric"
    #   - "RealWorldDataMart-fabric"
    FABRIC_ID = "RealWorldDataMart-fabric"

    try:
        fabric_btn = wait.until(EC.element_to_be_clickable((By.ID, FABRIC_ID)))
        fabric_btn.click()
    except Exception:
        # fallback: choose by visible text if ID changes
        xpath = f"//span[normalize-space()='{FABRIC_ID.replace('-fabric','')}']/ancestor::button"
        fabric_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        fabric_btn.click()

    # small buffer for the page to load
    time.sleep(2)

    # screenshot before quit (as you requested)
    take_screenshot(driver, "select_fabric_opened")

    driver.quit()