from pages.login_page import LoginPage

def test_tenant_validation(driver, config):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.enter_tenant("wrongtenant")
    lp.click_proceed()
    page = driver.page_source.lower()
    assert "tenant" in page and ("invalid" in page or "not found" in page)