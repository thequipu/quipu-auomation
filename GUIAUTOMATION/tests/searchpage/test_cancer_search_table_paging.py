import os
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.search_page import SearchPage

@pytest.mark.search
def test_cancer_functional(driver, config):
    wait = WebDriverWait(driver, 20)

    # -------------------- setup + login --------------------
    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_id(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password(config["password"])
    lp.click_login()

    # -------------------- fabric selection (exact IDs + sleeps) --------------------
    sp = SearchPage(driver, wait)
    sp.open_hetionet_fabric()

    # -------------------- search page ----------------------
    sp.type_search_and_submit("cancer symptoms")
    sp.click_table_view()

    # optional: mirror your original (commented) screenshot lines
    # os.makedirs("artifacts/screens", exist_ok=True)
    # driver.save_screenshot("artifacts/screens/cancer_symptoms.png")

    # keep page a moment if you want
    # time.sleep(2)

    # You asked to keep driver.quit in scripts—doing it here explicitly.
    driver.quit()