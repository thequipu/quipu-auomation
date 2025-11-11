# tests/schema/test_addnew_nodeclick.py
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.schema_page import SchemaPage

@pytest.mark.schema
def test_addnew_nodeclick_flow(driver, config):
    wait = WebDriverWait(driver, 25)

    # Login
    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_and_proceed(config["tenant"])
    lp.login(config["username"], config["password"])

    sp = SchemaPage(driver, wait)
    sp.open_menu()
    sp.goto_schema()

    # Add New Schema -> open workspace
    sp.open_add_new_schema()
    sp.fill_new_schema_form(name="K1", prefix="K11", description="nani")
    sp.create_schema_open_workspace()

    # Typeahead select sources
    sp.search_datasource_in_typeahead("KYC_MINI", press_enter=True)
    time.sleep(2)

    # Select all in side panel and Done
    sp.select_all_sources_in_sidepanel()
    sp.sidepanel_done()

    # (Canvas click logic in your raw script is best kept separate; here we stop at selections)
    # Capture one screenshot and return
    sp.screenshot("schema_addnew_nodeclick")

    # logout
    lp.logout()