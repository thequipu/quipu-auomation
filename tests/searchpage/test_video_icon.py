import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.search_page import SearchPage

@pytest.mark.video
def test_video_icon_click(driver, config):
    wait = WebDriverWait(driver, 30)

    # login
    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_id(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password(config["password"])
    lp.click_login()

    sp = SearchPage(driver, wait)
    sp.open_fabric_menu("Hetionet")  # your previous flow
    sp.click_video_icon()            # raises if it can't find/click