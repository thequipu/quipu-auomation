# tests/schema/test_create_version.py
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.schema_page import SchemaPage

@pytest.mark.schema
def test_create_version_flow(driver, config):
    wait = WebDriverWait(driver, 25)

    # Login
    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_and_proceed(config["tenant"])
    lp.login(config["username"], config["password"])

    sp = SchemaPage(driver, wait)
    sp.open_menu()
    sp.goto_schema()

    # Open Add Schema (tab contains Create Version)
    sp.open_add_new_schema()
    sp.open_create_version_tab()

    # Select existing schema + version
    sp.select_schema_in_create_version("schema-option-200MDATA")
    sp.select_version_in_create_version("schema-version-option-556")

    # Fill names & descriptions
    sp.fill_create_version_names(new_schema_name="K2",
                                 new_desc="krishna",
                                 version_desc="Krish")

    # Create
    sp.create_version_submit()
    time.sleep(2)

    lp.logout()