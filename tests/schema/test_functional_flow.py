# tests/schema/test_functional_flow.py
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.schema_page import SchemaPage

@pytest.mark.schema
def test_schema_functional_flow(driver, config):
    wait = WebDriverWait(driver, 25)

    # Login
    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_and_proceed(config["tenant"])
    lp.login(config["username"], config["password"])

    sp = SchemaPage(driver, wait)
    sp.open_menu()
    sp.goto_schema()

    # Open a schema tile
    sp.open_schema_by_id("csv6tablesdios-schema")
    time.sleep(1)

    # Toolbar actions
    sp.zoom_out_double()
    sp.zoom_in_double()
    sp.fit_to_screen()

    # Node config panel open → open details → screenshot → back
    sp.open_node_config_panel()
    sp.open_node_configuration()
    sp.screenshot("schema_flow")
    sp.back_from_node_config()

    # Edit schema toolbar → open similarity → screenshot
    sp.click_edit_schema_toolbar()
    sp.open_similarity_view()
    sp.screenshot("similarity_view")

    # Return to schema list
    sp.back_to_workspace()
    sp.back_to_schema_list()

    # Edit from tile, set description, toggle versions, save, reopen, close
    sp.edit_schema_by_tile("csv6tablesdios-schema-edit")
    sp.set_schema_description("schema")
    sp.toggle_versions_accordion()
    sp.save_schema_dialog()
    sp.edit_schema_by_tile("csv6tablesdios-schema-edit")
    sp.close_schema_dialog()

    # Logout
    lp.logout()