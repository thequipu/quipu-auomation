import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.multimedia_page import MultiMediaSearchPage
from utils.screenshots import take_screenshot

def test_register_person_flow():
    cfg = DriverFactory.load_config()
    driver = DriverFactory.get_driver(cfg)
    wait = WebDriverWait(driver, int(cfg["timeouts"]["explicit"]))

    try:
        lp = LoginPage(driver, wait)
        lp.open(cfg["base_url"])
        lp.enter_tenant(cfg["tenant"])
        lp.click_proceed()
        lp.enter_username(cfg["username"])
        lp.enter_password(cfg["password"])
        lp.click_login()

        mms = MultiMediaSearchPage(driver, wait)
        mms.open_via_menu()
        mms.click_register_user()
        mms.record_and_stop()
        mms.fill_person_details("krishna", "krishna")
        mms.start_webcam()

        take_screenshot(driver, "video_uploaded")

        mms.logout()

        assert "login" in driver.current_url.lower() or "logout" in driver.current_url.lower()
    finally:
        driver.quit()