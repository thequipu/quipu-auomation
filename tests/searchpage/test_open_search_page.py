import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.search_page import SearchPage

@pytest.mark.smoke
def test_open_search_page(driver, config):
    wait = WebDriverWait(driver, 25)

    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_id(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password(config["password"])
    lp.click_login()

    sp = SearchPage(driver, wait)
    # at least search icon or search box should be visible
    try:
        wait.until(EC.visibility_of_element_located((By.ID, "search-menu")))
    except Exception:
        wait.until(EC.visibility_of_element_located((By.ID, "search-query")))