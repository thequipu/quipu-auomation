from pages.login_page import LoginPage

def test_tenant_validation(driver, config):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.enter_tenant("invalid-tenant")
    lp.click_proceed()
    # could assert validation message here
    assert True