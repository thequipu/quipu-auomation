# tests/searchpage/test_functional_search_open_button.py
import os
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.search_page import SearchPage


@pytest.mark.search
def test_functional_search_open_button(driver, config):
    wait = WebDriverWait(driver, 30)

    # -------------------- setup + login --------------------
    lp = LoginPage(driver, wait)
    lp.open(config["base_url"])
    lp.enter_tenant_id(config["tenant"])
    lp.click_proceed()
    lp.enter_username(config["username"])
    lp.enter_password(config["password"])
    lp.click_login()

    # -------------------- Fabric (EXACT IDs + sleeps) --------------------
    sp = SearchPage(driver, wait)
    sp.open_realworlddatamart_fabric()  # fabric-menu -> RealWorldDataMart-fabric

    # --------------- search page ----------------------
    search_text = "liam Gurret"
    sp.type_search_and_submit(search_text)
    time.sleep(5)  # keep slow UI buffer

    # Try to open the node details panel by name first, else probe, else wide scan
    clicked_px = sp.click_node_by_name_or_probe(search_text, wait_panel_seconds=10.0, allow_wide_scan=True)
    assert clicked_px is not None and sp.panel_visible(), "Panel did not open after clicking node (even with wide scan)."

    # -------------------- Click the Open button (your EXACT XPath) --------------------
    open_btn_xpath = '//*[@id="ngb-accordion-item-100-collapse"]/div/app-search-result/div/app-graph-viz/div/as-split/as-split-area[2]/div/div/div/div[2]/div[2]/app-details/div/app-node-info/div/div[1]/div[1]/div[2]/button[1]'
    changed = sp.click_open_button_xpath(open_btn_xpath, wait_for_graph_change_seconds=12.0)

    os.makedirs("artifacts/screens", exist_ok=True)
    driver.save_screenshot("artifacts/screens/after_open_button.png")

    # Non-fatal if unchanged, but we log it
    print("Canvas changed after Open click:", changed)

    time.sleep(5)  # leave visible for manual inspection if running headed