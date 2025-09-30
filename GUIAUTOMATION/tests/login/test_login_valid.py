from pages.login_page import LoginPage

def test_login_valid(driver, config):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.enter_tenant(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password(config["password"])
    lp.click_login()

    assert "http" in driver.current_url.lower()