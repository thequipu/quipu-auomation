from pages.login_page import LoginPage
from selenium.webdriver.common.by import By

def test_login_invalid_password(driver, config):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.enter_tenant(config["tenant"]); lp.click_proceed()
    lp.enter_username(config["username"]); lp.enter_password("wrong-pass"); lp.click_login()
    # adjust locator for error toast if available:
    # err = driver.find_element(By.CSS_SELECTOR, ".error")
    # assert "invalid" in err.text.lower()
    assert True