import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage


@pytest.mark.login
def test_login_invalid_password(driver, config):
    wait = WebDriverWait(driver, 20)
    lp = LoginPage(driver, wait)

    lp.open(config["base_url"])
    lp.enter_tenant_id(config["tenant"])
    lp.click_proceed()

    lp.enter_username(config["username"])
    lp.enter_password("WRONG_PASSWORD_123")
    lp.click_login()
    time.sleep(1)

    # Expect NOT to reach home
    try:
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, "fabric-menu")))
        assert False, "Login should fail with invalid password"
    except TimeoutException:
        assert True