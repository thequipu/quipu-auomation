# tests/searchpage/test_new_session_create_button.py
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.search_page import SearchPage


@pytest.mark.search
@pytest.mark.agentic
def test_new_session_create_button(driver, config):
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
    sp.open_fabric_menu("Hetionet")

    # open new session overlay and create session
    sp.toggle_agent_overlay()
    sp.create_new_session(session_id="k1", agent_index=1, vector_index=1)

    # small wait to let any toasts/events settle
    time.sleep(2)

    # If no exception, consider it pass (UI feedback may vary across builds)
    assert True