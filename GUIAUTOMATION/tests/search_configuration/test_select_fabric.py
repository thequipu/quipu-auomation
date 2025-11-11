# tests/search_configuration/test_select_fabric.py
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.search_config_page import SearchConfigPage

@pytest.mark.search_config
def test_select_fabric_configure_person_and_corporation(driver, config):
    wait = WebDriverWait(driver, 25)

    # -------- Login --------
    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_and_proceed(config["tenant"])
    lp.login(config["username"], config["password"])

    sc = SearchConfigPage(driver, wait)
    sc.open_menu()
    sc.goto_search_configuration()

    # -------- Fabric select --------
    sc.open_fabric_dropdown()
    sc.select_fabric_by_id("dbtrealworlddatamart")

    # -------- Person: toggle fields, save --------
    sc.open_entity_section("person")
    person_ids = [
        "Person Node-cb",
        "Person's Email-cb",
        "Person's Telephone Number-cb",
        "Person's Physical Address-cb",
        "Person's Security Holdings-cb",
        "Person's Security Transactions-cb",
        "Person's country of citizenship and place of birth-cb",
    ]
    sc.toggle_checkboxes_by_ids(person_ids, pause=0.5)
    # Your original script toggled twice; keep behavior to mirror UI state changes
    sc.toggle_checkboxes_by_ids(person_ids, pause=0.3)
    sc.click_save_for_entity("person-save")

    # -------- Corporation: open first query, scroll, save & close E360 path --------
    sc.open_entity_section("corporation")
    sc.open_corporation_query_header()
    sc.scroll_to_bottom()
    sc.save_e360_path()
    sc.close_e360_path()

    # -------- Logout --------
    lp.logout()