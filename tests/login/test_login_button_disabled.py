import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage


@pytest.mark.login
def test_login_button_disabled(driver, config):
    wait = WebDriverWait(driver, 20)
    lp = LoginPage(driver, wait)

    lp.open(config["base_url"])
    lp.enter_tenant_id(config["tenant"])
    lp.click_proceed()
    time.sleep(1)

    # Sign-in button before entering username/password
    sign_in = wait.until(EC.presence_of_element_located((By.ID, "signIn-btn")))
    disabled_attr = sign_in.get_attribute("disabled")

    # If disabled attribute exists -> assert disabled
    if disabled_attr is not None:
        assert disabled_attr in ("true", "disabled", ""), "Sign-in should be disabled before credentials"
        return

    # If not disabled, a click should NOT log us in without creds
    sign_in.click()
    time.sleep(1)

    # Verify we did NOT land on home (fabric-menu) within a short window
    try:
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID, "fabric-menu")))
        assert False, "Reached home without credentials; sign-in should not allow this"
    except TimeoutException:
        assert True