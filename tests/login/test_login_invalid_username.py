from pages.login_page import LoginPage

def test_login_invalid_username(driver, config):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.enter_tenant(config["tenant"])
    lp.click_proceed()
    lp.enter_username("wrong_user")
    lp.enter_password(config["password"])
    lp.click_login()

    # Soft validation: page shows error text or stays on login
    page = driver.page_source.lower()
    assert "invalid" in page or "incorrect" in page or "error" in page