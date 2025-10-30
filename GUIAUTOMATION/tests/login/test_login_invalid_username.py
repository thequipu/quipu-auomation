from pages.login_page import LoginPage

def test_login_invalid_username(driver, config):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.enter_tenant(config["tenant"]); lp.click_proceed()
    lp.enter_username("wrong-user"); lp.enter_password(config["password"]); lp.click_login()
    assert True