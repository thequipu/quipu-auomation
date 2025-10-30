from pages.login_page import LoginPage
from selenium.webdriver.common.by import By

def test_login_button_disabled(driver, config):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.enter_tenant(config["tenant"]); lp.click_proceed()
    # leave username/password empty to check disabled
    btn = driver.find_element(By.ID, "signIn-btn")
    # if site enables by default, this will need change
    assert not btn.is_enabled()