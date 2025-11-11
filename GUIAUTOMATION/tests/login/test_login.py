# tests/login/test_login.py
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage


@pytest.mark.login
def test_login_and_logout(driver, config):
    wait = WebDriverWait(driver, 20)

    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])

    # tenant + creds + sign in (keep sleeps)
    lp.enter_tenant_id(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password(config["password"])
    lp.click_login()

    # assert landed (fabric menu visible)
    home = lp.wait_for_home()
    assert home.is_displayed(), "Login did not reach the home (fabric menu not visible)."

    time.sleep(1)

    # optional, best-effort logout (won't fail test if missing)
    lp.try_logout()
    time.sleep(1)