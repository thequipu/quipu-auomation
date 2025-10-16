import time
from pages.login_page import LoginPage

def test_login_invalid_password(driver, config):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.enter_tenant(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password("wrongpass")
    lp.click_login()
    time.sleep(2)
    page = driver.page_source.lower()
    assert "invalid" in page or "incorrect" in page or "error" in page